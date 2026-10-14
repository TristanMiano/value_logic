# Three elementary dependence-robust survival bounds

Codex (GPT-6), DEVELOPMENT, 2026-10-14.

For integer scores0,1,2 and a k-query prefix with common marginal p, write
S=n1+2n2, Z=n1+n2 and H=n2. If failure S<Q occurs then
S<=Q-1, Z<=Q-1 and H<=floor((Q-1)/2). Their unrestricted maxima are 2k,k,k.
Whenever denominator M-h is positive, the affine function (M-X)/(M-h) is at
least1 on X<=h and nonnegative on every possible outcome. Thus it majorizes
the failure indicator whenever failure implies X<=h. Taking expectations gives

```math
U_k\le\min\left\{1,
\frac{2k-k(p_1+2p_2)}{2k-Q+1},
\frac{k-k(p_1+p_2)}{k-Q+1},
\frac{k-kp_2}{k-\lfloor(Q-1)/2\rfloor}\right\},
```

omitting nonpositive-denominator terms. These are valid upper bounds for any
dependence. They require only marginal means of three bounded counts, with no
independence or expensive probability compiler. The minimum is taken over
expected values of separately valid majorants; it is not an expectation of the
pointwise minimum with incorrectly pooled moments. Each chosen affine plane can
also be checked directly against the integer lattice.

Compare against all1152 already prospectively selected dep03 exact certificates.
This is an analytical explanation of observed results; it is not a new blind
holdout and does not prove these three bounds always attain the sharp LP value.
Where the bound is weaker it remains a valid candidate for a cheap robust
prefix policy. A separate fresh service measurement is still needed to price
all source setup, policy use and final checks together. Do not transfer dep01's
analytical fee savings directly into an application cost claim.
