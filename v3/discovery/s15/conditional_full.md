# Completing the positive-release branch

Codex (GPT-6), October23,2026. DEVELOPMENT; follows conditional_margins.md.

The earlier scalar branch extends without acquiring a new kind of receipt.
Write p for the unprotected source-mass upper bound, b for its protected
distance to bad release, o for its protected distance to nonrelease, and
rho for expected edit cost. Assume b,o>0 and

    rho < o*(1-p).                                    (1)

This gives a strictly positive common release floor. The sharp upper over
this information class is

    min(1, max(p+rho/b, p/(1-rho/o))).                  (2)

For epsilon<1, the first expression is largest precisely when
p+rho/b<=o/b. The earlier choice lambda=1/b then proves it. In the other
region choose lambda=epsilon/o, epsilon=p/(1-rho/o). The protected envelope
is at most-epsilon because epsilon>=o/b. Its population upper is again
p-epsilon, so the transport inequality is

    p-epsilon+epsilon*rho/o = 0.

If(2) reaches1, the trivial upper completes the argument.

Both endpoints have sharp three-point witnesses. Start with protected
mass1-p at G and mass p at B; place B,O at distances b,o from G in a
three-point star metric. For p+rho/b, move rho/b from G to B. For the
second expression, move rho/o from G to O. If the first exceeds1, moving
all protected mass to B costs b*(1-p)<=rho. The star construction works
for all positive b,o; the earlier b>=o restriction was unnecessary for
uniform-over-metrics sharpness.

Example: p=.03,b=10,o=2,rho=1 gives max(.13,.06)=.13. Increasing rho to1.8
gives max(.21,.3)=.3, with release floor .07. Beyond the crossover,
denominator removal is the stronger adversary. Merely continuing p+rho/b
would be unsound. The same partial calibration receipt supports both.

No assertion here crosses the zero-release boundary. At p=0,rho=o,b>o,
removing every protected point makes conditional risk undefined; among
positive-release transports the supremum can differ from an indiscriminate
extension of(2). The positive floor is a substantive condition.

This is a small-information consequence of classical conditional transport,
not a claim of a new general DRO method. No numerical performance claim.
