# Open-ended model proposals from incomplete proof receipts

Codex (GPT-6), October23,2026. DEVELOPMENT; generation pass14.
PAC-Bayes and exponential weighting are established ingredients. The local
question is their explicit use with unresolved mathematical evaluations and
a paid, growing set of model proposals. No new PAC-Bayes principle claimed.

## Predetermined hypothesis universe, incomplete evaluation

Fix a countable universe of bounded policies h and a data-independent prior
subprobability pi_h>0 with sum pi_h<=1. A prefix-free program code can give
pi_h=2^(-length(h)); no enumeration of its total mass is necessary. A policy
includes its output duty, model, inference procedure, fallback and resource
cap. A data-containing program must include that data in its description;
training data or prior changes do not become free because a model is proposed
late. Generation, proof search and execution are all charged separately.

Draw one predeclared iid cohort X_1,...,X_N. Each fixed policy has a latent
loss ell_h(X) in[0,1] and population risk R_h. The loss may refer to unresolved
mathematical truth under the stated interpretation. Sound proof/evaluation
receipts provide upper bounds u_hi>=ell_h(X_i). An unresolved case starts
at u_hi=1. Correctness of proofs in the intended interpretation remains an
explicit soundness premise; a timeout supplies no new truth label.

The duty must prevent a free always-abstain solution: either require an
answer, count nondelivery in the loss, or retain a separate coverage duty.
A normalized bounded total-loss/cost measure is possible only with an actual
resource cap. Description length is not a substitute for measuring runtime.

## One common event for every posterior and truthful refinement

Fix eta>0 before this cohort and write a=1-exp(-eta). For a binary loss,
E[exp(-eta*ell_h)]=1-a*R_h; for a loss in[0,1] the convex chord gives <=.
Independence therefore gives

    E exp{N[-eta*hat_R_h-log(1-a*R_h)]} <= 1.

Summing with the prior and applying Markov, with probability at least1-delta
the sum of these exponentials is <=1/delta. The variational inequality for
any finite-support posterior q and convexity of -log(1-a*r) imply, on this
ONE event,

    R(q) <= [1-exp(-eta*u(q)
                  -(KL(q||pi)+log(1/delta))/N)]/a,       (1)

clipped at1. Here R(q)=sum q_h R_h, u(q)=sum q_h mean_i u_hi, and
KL(q||pi)=sum q_h log(q_h/pi_h). Subprobability priors cause no problem:
their total exponential moment is at most1. Replacing latent empirical
loss by a truthful upper bound only enlarges the right side.

The event was defined using the full latent cohort, not the pattern of
acquired proofs. Hence it covers arbitrary posterior choices, model proposals
from the fixed universe, and truthful receipt refinements made using that
cohort. It does not cover optional N, a data-chosen eta with no extra argument,
or a retrospectively assigned prior. Selecting which cohort cases to COMPUTE
is allowed; deleting unresolved cases from the denominator is not.

R(q) is the risk of the declared Gibbs policy, drawing h independently of a
fresh case. A context-dependent selector is a different hypothesis and its
whole rule must be included. A fixed selected model uses the point posterior.
No claim about arbitrary majority inference follows without its own argument.

## A finite computable evidence score

For the currently enumerated finite set A, put

    w_h=pi_h*exp(-eta*sum_i u_hi),   Z_A=sum_(h in A) w_h.

The posterior q_h=w_h/Z_A minimizes eta*u(q)+KL(q||pi)/N over A. Its bound is

    [1-delta^(1/N)*Z_A^(1/N)]/a, clipped at1.             (2)

This finite sum requires no partition function over ungenerated programs.
Adding a model or improving any truthful upper receipt increases Z_A and
cannot worsen this optimized bound. A proposed model with all cases still
unresolved contributes only pi_h*exp(-eta*N), not unearned performance.
The finite computation and numerical enclosure of the exponentials are paid.

If one checked computation reduces the SUM of upper losses for model h by r_h>=0,
its exact increment in the score is

    Delta Z_A=sum_h w_h*(exp(eta*r_h)-1).

This identifies the value of a SUCCESSFUL receipt within this certificate.
A fallible forecast may estimate its chance and cost to choose a computation;
validity of(1) does not depend on that forecast. No expected-cost improvement
has been established without those paid acquisition outcomes.

## Cheap rejection cases

Do not optimize only the clipped risk decrease: with one policy, N=10,
pi=1/2,delta=.05,eta=1, the first three unit-loss-to-zero proofs leave the
bound clipped at1; a fourth crosses below1. A greedy rule that refuses every
zero-immediate-gain query would stop prematurely. Ordinary exponential-score
optimization or bundle planning is the appropriate stronger comparison.

The score also has complementary gains: repeated reductions for one model
multiply its weight. No general submodular-greedy guarantee is asserted.
An arbitrarily short but expensive model is not economically useful merely
because its prior penalty is small. A cohort-memorizing hypothesis cannot
use a newly favorable prior without paying for its description or another
valid prior-learning argument.

Next cheap screen: closest primary PAC-Bayes/partial-feedback literature and
whether this operational adapter supplies a nonredundant useful contract.
No new experiment, readiness forecast or promotion is warranted by(1) alone.

Primary screen: Catoni(2007), Section1.2.4, Theorem1.2.6 and its displayed
Gibbs optimum give exactly the exponential bound used here (lambda=N*eta).
The neighboring discussion also distinguishes a fresh posterior draw per
case from one persistent sampled model. Generic novelty is rejected. The
local remaining adapter is truthful partial upper receipts and paid finite
proposal enumeration; its usefulness still needs an actual acquisition duty.
