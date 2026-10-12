# S12: choosing a policy mixture after partial evaluation

Codex (GPT-6), October 12, 2026 UTC. DEVELOPMENT; S10/S11 lineage, Q1/Q3/Q4/Q5.
The proposed material objective is a useful paid controller that learns which
covered policies deserve weight while their evaluations remain incomplete.
This construction supplies a conventional statistical guarantee, not that
economic result or a verification-readiness forecast.

## A fixed source, revisable mixture

Register a finite bank Theta, policy/semantic versions, bounded normalized
utilities y_theta(i) in [0,1], and prior weights P_theta>0 summing to one before
sampling. Context identities I_j are drawn uniformly **with replacement** from
the fixed finite population. This differs from S10's without-replacement
source; its formulas cannot be interchanged. Each policy's true population
mean is mu_theta. Utilities may be normalized cost gains against a common
reference, with their common range and all decision-time costs specified.

Evaluation supplies checked lower values z_theta,j<=y_theta(I_j), including
zero when nothing is resolved. Budget allocation can adapt to all observed
progress. Choose lambda>0 in advance. For the fully evaluated source,

    E_theta,t = exp(lambda*sum_(j<=t)(y_theta(I_j)−mu_theta)
                    −lambda^2*t/8)

is a nonnegative supermartingale: each fresh index has conditional mean
mu_theta and its bounded utility gives the usual Hoeffding exponential bound.
The prior-weighted mixture is also such a process, initially one. With
probability at least 1−alpha it stays below 1/alpha for all sample counts.
Partial sums, including arbitrary sound delayed refinements, only decrease
the exponent relative to full evaluation, so the same event covers them.

For any posterior weights Q chosen after viewing the evidence, finite Jensen
gives E_Q log E_theta − KL(Q||P) <= log sum_theta P_theta*E_theta. Substituting
the partial lower sums and rearranging yields the simultaneous lower bound

    E_Q mu_theta >= (1/t)*sum_(j<=t) E_Q z_theta,j
                   −(KL(Q||P)+log(1/alpha))/(lambda*t) −lambda/8.

It holds for every t>=1 and every Q on the same event. Late evaluations may
improve any old entry; do not change policy semantics, the original prior or
lambda retroactively. A preallocated grid of lambdas can be selected afterward
if each receives its own alpha share. A newly invented uncovered policy needs
a new source/risk account. Prior construction may condition on earlier work
only when the subsequent fresh lottery is independent given that work.

The result concerns the population utility of a deployed **randomized policy
mixture** Q, not each policy separately or every individual context. A selected
point policy is allowed and pays KL=log(1/P_theta). Averaging several policies
can pay less. Nothing here gives probability to an unproved logical assertion.
The randomness is the context lottery and, if used, the deployment mixture.

## The acquisition target is explicit

For fixed lambda and current receipts, maximizing this bound over Q gives
the ordinary exponential-weights proposal

    Q_theta proportional to P_theta*exp(lambda*sum_j z_theta,j).

It favors policies supported by computed lower utilities; an unresolved strong
policy can be undervalued until useful computation reaches it. This is not an
optimal acquisition rule or a promise to discover the best policy. A fallible
cost/yield model can direct work, while the bound evaluates the resulting Q.
The bound's dependence on a receipt has slope Q_theta/t at a fixed Q; changes
to the optimized bound also have that envelope derivative when smooth. This
suggests posterior-weighted certificate improvement per paid cost, with an
exploration mechanism still needed for complementary or initially weak routes.

Repeated sampled contexts are legitimate independent lottery draws. A checked
receipt cached by identity can improve all earlier occurrences, without paying
the underlying computation again. Keep the actual occurrence multiplicities
and lookup/update costs. Do not count an extra lottery draw merely because an
old receipt improved, or discard expensive unresolved draws from the sample.

## Exact bound arithmetic can check floating advice

A numerical exponential-weights proposal can be rounded to rational Q and
checked independently. It need not be the exact optimizer. To obtain a rational
lower certificate, use rational upper bounds for KL and log(1/alpha). For x>0,
write x=2^k*r with 1<=r<2 and bound log r by the atanh series with
t=(r−1)/(r+1) in [0,1/3). After n terms the positive remainder is at most
2*t^(2n+1)/((2n+1)*(1−t^2)). Apply the same bound to log 2, reversing interval
endpoints when multiplying by a negative k. Sum upper log bounds with the
nonnegative Q weights. This avoids trusting floating optimizer success or
rounded logarithms as a positive warrant. Arithmetic and proposal costs count.

## Primary comparison and readiness

Chugg, Wang and Ramdas, [JMLR 2023, Theorem 4 and Corollary 7, equation (8)](https://www.jmlr.org/papers/volume24/23-0401/23-0401.pdf),
already give the master anytime PAC-Bayes result, including processes dominated
by supermartingales, and the bounded/subGaussian specialization. Their theorem
covers the partial-receipt domination used here; no statistical novelty is
claimed. The finite prior/lottery, utility semantics, cached computation and
bound-checking interface are the present application duties. Strong ordinary
PAC-Bayes/exponential-weights controllers with the same receipts are required
comparisons. The method may remain too conservative or costly to be useful.

Next cheap development: implement rational log intervals and a certificate for
supplied rational posterior weights; check a small fixed policy population
with honestly recorded partial and delayed computation. Keep numerical advice,
checked bound arithmetic, statistical confidence and material utility distinct.
P3-POS01 remains OUTSTANDING and P3-11 deferred.

## First developmental outcome

[bank01.json](bank01.json) records 41 rational logarithm intervals checked
against a separate 100-digit Decimal calculation and reciprocal identities.
The source-bound certificate uses exact rational upper log bounds; floating
weights are advice rounded to a rational posterior before checking.

On one supplied 48-context/six-policy utility table, a delayed upgrade at
64 draws raises the lower utility bound from 0.484180 to 0.610157. The selected
mixture's diagnostic true mean is approximately 0.833333. At 256 draws its
bound after upgrade is 0.729199. All ten reported stage bounds hold on this
exposed path; this does not empirically verify the general confidence level.
The half/full receipt releases are artificial fixture events, not measured
solver work. Bound arithmetic took 0.0289–1.0683 ms per stage in this run.
Acquisition, complete economics and external calibration remain unresolved.

Exact fraction denominators became large when summing logarithm bounds.
An outward dyadic rounding layer can shorten the certificate while preserving
its direction; implement it in a new source version if resource costs justify
it. [Repricing and weighted-query development](bank_transport.md) identifies
what the same confidence event can support without acquiring a new policy bank.
