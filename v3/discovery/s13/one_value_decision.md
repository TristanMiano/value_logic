# A decision from one value, without fitting the latent matrix

Codex (GPT-6), DEVELOPMENT, October21,2026. A worked use of the sharp
ordinary moment envelopes in one_value_bounds.md. No numerical-analysis
priority or real-world measurement-saving claim is made.

Let y(t)=b^T(A+t*UU^T)^(-1)b, with the positive spectral-measure contract
already warranted. Normalize y(0)=1. Suppose the spectral support is known
to lie in[0,1], and one exact purchased value gives y(1)=3/4. The strongest
upper envelope from that one moment is

    u(t)=3/(t+3),                 0<=t<=1,
    u(t)=1/2+1/[2*(t+1)],         t>=1.

For t<=1 the first expression is attained by the one-atom spectrum lambda1/3.
For t>=1 the second is attained by equal masses at lambda0 andlambda1.
Both satisfy the same baseline, support and purchased value. These are
realizable positive quadratic-response systems, not signed-measure examples.

Suppose an intervention level t>=0 costs t/20 and the remaining task loss is
y(t). A bounded reasoner that wants the smallest worst possible loss over
this entire compatible class can solve the scalar robust problem

    min_(t>=0) [t/20+u(t)].

On[0,1] its derivative is1/20-3/(t+3)^2<0. On[1,infinity) its derivative
is1/20-1/[2*(t+1)^2], which vanishes at

    t_star=sqrt(10)-1,
    robust loss=9/20+1/sqrt(10), approximately0.766227766.

The second derivative is positive, so this is the global minimizer. Keeping
the measured intervention t1 gives robust loss4/5. The exact improvement is
7/20-1/sqrt(10), approximately0.033772234 loss units. No percentage is used
to suggest a measured workload advantage. The worst-case spectrum above
attains the reported value, so this is the exact optimum for the stated
moment class, not merely an upper-bound minimization with an unknown gap.

A fitted one-atom model also matches y(1), but would choose t=sqrt(60)-3.
That choice is unwarranted as the robust optimum because another matching
model has a different entire intervention curve. The moment-based ordinary
optimizer exactly reproduces t_star and its guarantee; it is the strong
comparison, not a baseline the Value Logic notation outperforms.

What this contributes to the search is an explicit decision duty for the
numerical adapter. More observations are needed only if their possible
decision improvement justifies their price. The support bound, positivity,
stable response mechanism, exact receipt and monetary/loss conversion were
supplied; the construction does not acquire or validate them for free.
No inference about unbounded arithmetic truth or arbitrary interventions
follows from this example.
