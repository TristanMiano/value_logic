# S14: newly proposed programs inside an old statistical source

Codex (GPT-6), October 12, 2026 UTC. DEVELOPMENT; readiness unassessed.

## A constructive answer to the changing-menu obstacle

The finite S12 bank cannot simply add a data-chosen policy with a newly
renormalized prior. A different, prospectively fixed source can cover a
countable program family from the start. Fix a bounded, terminating policy
language, immutable operational semantics and environment, a prefix code for
programs, an iid context law, and a versioned bounded utility map Y_p(X) in
[0,1]. Programs may be discovered or constructed after seeing context data;
every possible code already names a fixed function in the family. A program
cannot silently read mutable sample history or change the environment. Any
data-dependent literal, lookup table or new rule belongs in its code.

For code length ell(p), Kraft's inequality supplies subprior w_p=2^-ell(p),
with sum_p w_p<=1. Unused mass can be assigned to a dummy zero-utility program.
For each fixed p, the full-information oracle

    E_p,t = exp(lambda*sum_{j<=t}(Y_p(X_j)-mu_p)-lambda^2*t/8)

is a nonnegative supermartingale. Its countable weighted mixture has initial
expectation at most one (nonnegative sums justify monotone convergence).
The ordinary mixture/Ville/change-of-measure argument therefore covers every
finite-support posterior Q and every t on a common event of probability 1-alpha:

    E_Q mu_p >= E_Q S_p/t
              - [sum_p Q_p log(Q_p/w_p)+log(1/alpha)]/(lambda*t)
              - lambda/8.

Here S_p can use checked partial lower evaluations of any of the already drawn
contexts, including evaluations performed only after p was proposed. They are
pointwise dominated by the oracle's full sums. Uncomputed values remain zero.
Retroactive evaluation is permitted by this prospective all-program event;
retroactively inventing the language/prior to make the selected program short
is not. A countable family need not be executed or explicitly enumerated to
define the source, but every queried receipt must still be computed and checked.

This is a direct descriptive-policy application of the existing anytime
PAC-Bayes framework, not a new statistical theorem. Chugg, Wang and Ramdas
(2023), Theorem 4 pp. 10-11 and Corollary 7 pp. 13-14, explicitly permit a
general data-free prior and adapted posteriors; their domination hypothesis
supplies the partial-evaluation step. These passages were read in the
[primary paper](https://www.jmlr.org/papers/volume24/23-0401/23-0401.pdf).
The earlier finite-bank exposures keep their original source and prior.

## Concrete prefix accounting

A simple general envelope for an n-bit program payload is gamma(n+1) followed
by exactly n payload bits, where gamma(k) is zero padding followed by the binary
representation of positive k. Its total length is n+2*floor(log2(n+1))+1.
The length headers are prefix-free, and a common header fixes payload length;
thus the full code family is prefix-free. Summing 2^-length over all payloads
reduces to sum_{n>=0}2^-length(gamma(n+1))=1, by grouping powers of two.
Only valid terminating programs need retain mass; invalid strings are unused.
Canonicalizing equivalent programs can avoid aliases, but any uncharged
data-driven dictionary or altered interpreter would change the source.

For a point posterior, its description penalty is ell(p)*log(2). For mixtures,
it is sum Q log Q + log(2)*E_Q ell. This can be computed using compact outward
log intervals without materializing an integer of size 2^ell. A sparse
description of a high-order value contrast can therefore be preferable to a
large lookup table, if it actually describes the operative policy and all
data-dependent constants. This is ordinary complexity control, not free
selection or a theorem that a short fallible model is true.

## Removing the fixed-lambda plateau prospectively

Fix lambda_k=2^-k for k>=0 and allocate alpha_k=alpha/[(k+1)(k+2)]. The alpha_k
sum to alpha. Every k-specific bound then holds on the same union-bound event,
so a checked query may select k after data. Its penalty uses log(1/alpha_k).
Increasing t can use smaller lambda without paying a constant lambda/8 floor.
The grid is an ordinary countable risk allocation; a retrospectively chosen
unpenalized lambda is not justified. The k>=0 grid may be weak for small t.

Ignoring grid overhead only for a planning approximation, minimizing
C/(lambda*t)+lambda/8 gives sqrt(C/(2t)), attained at sqrt(8C/t). To resolve an
empirical margin delta one therefore needs roughly t>C/(2*delta^2). For a
1,000-bit program, C is about 700 at conventional alpha, so a 0.05 margin can
require roughly 140,000 fully informative contexts even before grid overhead.
The countable construction repairs selection validity but can destroy the
economics. Useful shared grammars and reusable evaluation receipts must earn
their costs; this quantitative obstacle is a reason to keep the program's
material claim unassessed.

## Next constructive checks

Check prefix encoding and exact penalty arithmetic, then demonstrate code
discovery after a genuinely fresh development lottery with its source committed
first. Include a memorizing program to expose description costs. This can test
the implementation and illustrate bounds, not confirm general statistical
coverage or economic superiority. Relate any positive plan certificate to its
actual deployment gain and include source construction/evaluation expenses.

## Cheap prospective development exposure

[program01_plan.json](program01_plan.json) was written before the fresh lottery,
binding code, an eight-bit context space, deterministic parity labels, seed,
prefix prior and lambda-risk grid. [program01.json](program01.json) contains
2,047 prefix encode/decode and pairwise-prefix checks, then eight selected-code
stages. Programs were proposed after seeing data and evaluated retrospectively
on the drawn contexts; reused contexts were counted only at their actual
lottery multiplicities. The 18-bit fitted parity program's bound exceeds 0.62
at t=64 and 0.90 at t=1024. A memorizing program fits the same samples, but its
1,034-bit description at t=1024 has a lower bound below 0.18 despite diagnostic
true accuracy 253/256. All eight realized bounds held on this exposed path;
that is not a validation of the general confidence level.

An idealized empirical accuracy of 0.55 first beat a 0.50 comparator on the
tested powers-of-two grid at t=8,192 / 32,768 / 262,144 for code lengths
32 / 128 / 1,024. The prototype took 16.040 ms excluding external evaluator or
deployment costs. These examples support the implementation and expose the
description-cost bottleneck. They do not establish useful external economics.
