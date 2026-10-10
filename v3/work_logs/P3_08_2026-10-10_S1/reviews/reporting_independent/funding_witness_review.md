# Independent derivation review: completion selection by provider funding

Status: **PASS with the explicit purchase protocol below.** This is a DEVELOPMENT review of the abstract proposal supplied by the principal, not a run of the CNF broker and not an independent theorem-proof campaign. Same-model, nonblind review; principal time credit: zero. No private episode labels or score archives were read.

## Finite probability space and report

There are $m=16$ blocks, each containing the deterministic labels $y=(0,1)$. In every position the forecast is $q=1$; hard reuse is off. One of the two positions is selected by a fresh independent fair bit in each block, with actual propensity $\pi=1/2$. Let $X$ count selections of the false-labelled position. On the full probability space of 16 fair bits,

\[
X\sim\operatorname{Binom}(16,1/2),\qquad T=32.
\]

The loss $d=(q-y)^2=1-y$ is one on the false position and zero on the true position. Consequently the total forecast loss is always $F=16$. The fixed-rate public construction under review gives

\[
A_c=\frac{T}{2}+\sum_{k=1}^{16}\frac{d_{J_k}-1/2}{\pi_{J_k}}
   =16+(2X-16)=2X,
\]

\[
U_c=\frac{T-m}{2}+\sum_{k=1}^{16}(\pi_{J_k}^{-1}-1)(d_{J_k}-1/2)=X.
\]

The realized unselected forecast loss is $V=16-X$. Since $q=1$, the randomized action is deterministic and its unselected loss is also $Z=16-X$. The common residual is therefore

\[
F-A_c=V-U_c=16-2X.
\]

Each block range parameter is $C_k=2$. Thus $Q=\sum_k C_k^2=64$, the declared fixed rate is $R=2\lceil\sqrt{32}\rceil=12$, and

\[
\rho=\frac{Q}{R}+\frac{5R}{8}=\frac{77}{6}.
\]

The specified $F$ interval misses exactly when \(|16-2X|>77/6\), equivalently $X\leq1$ or $X\geq15$. Its generic deterministic envelope, using the selected losses and the remaining per-position loss range, is \([X,X+16]\); intersecting with this envelope does not change those miss events. In particular the intervals at $X=0,1$ have upper endpoints $77/6$ and $89/6$, both below 16. This concerns this report construction, not every possible estimator using further structure of the deterministic block family.

There are $1+16=17$ fair-bit sequences in either tail. Hence the unconditional two-tail miss probability is

\[
\frac{34}{65536}=\frac{17}{32768}<\frac1{40}.
\]

## Purchase protocol required for the claimed completion event

Assign a deterministic checked-service price of two provider units to the first query in each block and one to the second. These are fixed public quotes attached to the query positions. After drawing the prescribed fair selector bit, the controller prepays the selected query's quote if its provider account can cover it. Otherwise it terminates with a partial failure record, preserving the spent prefix, without receiving that purchase's checked answer and without resampling, changing the quota, or issuing a completed-horizon report. Controller, fair-bit, storage and terminal-report obligations must be fully funded separately; the number 17 is only the provider account.

Under this protocol every completed path costs $2X+(16-X)=16+X$. All purchase costs are positive, so a provider budget of 17 completes exactly the paths with $X\leq1$. The probability of completion is $17/65536$; conditional on completion the specified $F$ interval misses with probability one. Fair bits after a partial failure can be regarded as unobserved coordinates of the original finite probability space, rather than draws actually performed after failure. Public prices happen to be correlated with labels in this deterministic example; the fixed $q=1$, hard-off controller is permitted to ignore that information.

A staged service with one paid unit before a possible second unit can give the same complete-path cost rule, provided a failed second stage preserves its spent first stage and yields no checked receipt. It must not obtain a private answer for free merely to decide the charge.

The reservation convention is material. If every purchase instead requires two units to be reserved *before* selecting its actual one- or two-unit completion price, a 17-unit account finishes only when the first 15 selected prices are one; the final price may be either one or two. The completion probability is then $2/65536$, not $17/65536$. Reserving the full 32-unit worst-case provider obligation at episode admission permits no episode with an account of 17.

The witness demonstrates how selecting completed reports by a truth-correlated resource cost can destroy conditional coverage despite a valid unconditional bound on the fully funded sampling experiment. It does not claim that 17 funds the actual broker, that provider units equal CNF tariff units, or that the unconditional bound itself fails. An all-path provider budget for this abstract service is 32, with the other obligations separately funded.
