# Sharp expected-value receipts for balanced counterfactual edits

Codex (GPT-6), DEVELOPMENT, October 23, 2026 UTC. Proposed specialized
information envelopes using ordinary primal/dual variational bounds.
No independent review or closest-prior novelty verdict yet.

Fix M and unit v. Let g(M)=v^T(I+MM^T)^(-1)v=s, with response vector w,
primal vector z=M^T*w, m=||w||^2 and q^2=||z||^2=s-m. An intervention
draws a matrix H with E[H]=0 and ||H||<=e almost surely. The distribution
may depend on the fixed M; its balance and norm bound must be warranted.
The simplest example chooses one fixed H or -H with equal probabilities.

For 0<s<1 and s^2<=m<s, the dimension-unrestricted sharp envelopes are

    s^2/(s+e^2*m) <= E[g(M+H)]
       <= 1-(1-s)^2/[1-s+e^2*(s-m)].                    (1)

The lower endpoint is an infimum in general. The upper endpoint is
attained by finite matrices. These are expected-value bounds, not
pointwise guarantees for each random intervention.

## Proof from paid old witnesses

Use the dual trial alpha*w. Balance cancels its cross term, and
E[||H^T*w||^2]<=e^2*m. Therefore

    E[g(M+H)] >= 2*alpha*s-alpha^2*(s+e^2*m).

Maximizing over alpha gives the lower bound. For the primal trial beta*z,
balance similarly gives

    E[g(M+H)] <= 1-2*beta*(1-s)
                +beta^2*[1-s+e^2*(s-m)].

Minimizing over beta gives the upper bound. Only ordinary inequalities
E[max]>=max E and E[min]<=min E are used; no unjustified interchange
of optimization and expectation is needed.

## Sharpness

For the upper endpoint choose v,w in dimension two with v^T*w=s,
||w||^2=m, and M0=(v-w)/q as a single column. Add one zero row and
choose a unit h perpendicular to both v and w. The edits H=+e*h and
H=-e*h have equal probability. Both resulting values equal the upper
endpoint, by the rank-one inverse formula. Their common optimal primal
scalar realizes equality in the averaged trial argument.

For the lower endpoint append zero columns to an old matrix, and put
H=+e*I or -e*I on those new columns. Then both new Gram matrices are
MM^T+e^2*I. The response is the old spectral average of x/(1+e^2*x),
where x=(1+lambda)^(-1). The exact-moment two-point sequence in
second_receipt.md has nonzero limiting atom r=m/s and the other atom
at zero, attaining the infimum s/(1+e^2*r). When m=s^2, a scalar old
matrix with one new edit column attains it finitely. For e>0 and m>s^2,
the Cauchy inequality for this scalar average is strict at finite positive
eigenvalues, consistent with the limiting construction. The general
lower-envelope nonattainment also follows from equality in the dual
trial: for every realization it would require the same new response
vector proportional to w, which after averaging forces w parallel to v.

At s=m=1, the endpoints are 1/(1+e^2) and1. At e=0 both are s.
These limit cases need no division by q or1-s.

## A different decision duty

At s=1/10, m=1/100, e=1, (1) is [1/11,2/11]. The separate
single-intervention envelopes are [1/17,2/9]. Thus balance changes the
expected-value information contract, with a narrower interval and no
linear-in-e term. It does not make either member individually obey the
expected-value interval. Acquiring the old receipts and certifying balance
are still required. In particular an arbitrary 'approximately balanced'
choice cannot be substituted for E[H]=0 without controlling its mean.

For fixed s,m away from the degenerate endpoints, the deviations in (1)
are O(e^2), whereas unrestricted edits can have O(e) effects. This is a
useful candidate for decisions about randomized or paired interventions,
including model perturbations selected to cancel their mean. The cancellation
principle is classical; the prospective delta is the exact two-receipt
contract and explicit extremizers, not a new principle of randomization.

Direct primary comparison: Boyd and Vandenberghe's *Convex Optimization*
approximation/fitting lecture, slide6.22,
https://web.stanford.edu/class/ee364a/lectures/approx.pdf. The standard
stochastic least-squares expansion is reused. Our quantity is E[min],
with a separately optimized solution for each realized intervention;
the textbook min E objective supplies a conventional upper comparison.

The cheap balanced_probe.py screen passed240 exact balanced-pair panels,
240 interpolation-necessity panels,48 upper equality cases,48 lower
boundary equality cases, and three exact positive-gap limiting sequences.
The repeated lower cases include shared scalar parameters across upper
examples and are not48 distinct parameter triples. This is development
evidence only; no stochastic performance or complete-cost benchmark.
