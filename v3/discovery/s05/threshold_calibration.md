# Calibrating a censored SAT threshold distribution

Contributor: **ChatGPT (GPT-6 Astra Pro)**. October 12, 2026 UTC.
DEVELOPMENT; a source specialization for the [session](session.md), not a
confirmation result. Principal-clock accounting remains with the principal.

## A threshold with checked interval observations

Each task i supplies a fixed clause chain
`F_0(i) subseteq F_1(i) subseteq ... subseteq F_m(i)` with common semantics.
Define H_i as its first UNSAT index, or m+1 if every formula is SAT. Thus
`H_i in {0,...,m+1}` and `F_k(i) is UNSAT iff H_i <= k`.

Retain a sound integer interval `[l_i,u_i]` containing H_i. Initially this can
be `[0,m+1]`. A checked SAT witness at index k permits
`l_i = max(l_i,k+1)`; a checked UNSAT certificate permits
`u_i = min(u_i,k)`. SAT witnesses transport to clause subsets and UNSAT
certificates to clause supersets through the appropriate checked bridge.
Charge proof production, checking and transport. A timeout narrows neither
endpoint unless it also produces a separately checked partial consequence.

Rows are sampled iid from a declared task source, or their identities are
drawn uniformly with replacement from a fixed finite cohort. Save every draw
before probing. Probe indices, order, budgets and revisits may adapt to all
previous results, including results already observed within the same row.
Never discard unresolved or expensive rows from the statistical denominator.

## Primary result actually read

**Henry W. J. Reeve (2024), A short proof of the
Dvoretzky–Kiefer–Wolfowitz–Massart inequality**, arXiv:2403.16651v1.
[Primary author paper](https://arxiv.org/pdf/2403.16651v1).
Read the iid setup, Theorem 1 and Corollaries 1–2, PDF pp. 1–3. Corollary 2
strengthens the classical uniform one-sided tail; applying the bound to both
directions gives the usual two-sided inequality below. The setup allows
discrete distributions, so ties among integer thresholds are permitted.
The confidence inequality is imported; the interval-receipt interface and
SAT interpretation are the proposed application. The original Massart (1990)
DOI/PDF could not be accessed directly and is not recorded as a full reading.

For the latent full empirical CDF `G_n(t)=sum_i 1[H_i<=t]/n` and population
CDF F, the imported two-sided DKW bound is

```text
P(sup_t |G_n(t)-F(t)| > e) <= 2*exp(-2*n*e^2).
e(n,delta) = sqrt(log(2/delta)/(2*n)).
```

## Pathwise envelope despite adaptive probing

At any stage of receipt refinement, define

```text
G_n^-(t) = sum_i 1[u_i <= t]/n.
G_n^+(t) = sum_i 1[l_i <= t]/n.
```

Since `l_i <= H_i <= u_i`, every row obeys
`1[u_i<=t] <= 1[H_i<=t] <= 1[l_i<=t]`. Consequently
`G_n^- <= G_n <= G_n^+` for every threshold t, on every possible probing
history. On the DKW event this gives the simultaneous population band

```text
L_n(t) = max(0, G_n^-(t)-e(n,delta)).
U_n(t) = min(1, G_n^+(t)+e(n,delta)).
L_n(t) <= F(t) <= U_n(t) for all t.
```

Set the known support endpoints exactly: F(-1)=0 and F(m+1)=1. Both empirical
envelopes are nondecreasing. Tightening a row interval raises G_n^- or lowers
G_n^+, so later proof receipts improve the same band without a new risk charge.
The latent DKW event does not mention the inspection policy. No independence
between censoring/probe choices and H is required for this domination argument.

For a **prespecified fixed n**, arbitrarily many further adaptive probes and
reports on those same n rows are covered by the same event. That is different
from choosing the sample count n after examining the data.

## An elementary anytime version

Allocate `delta_n=delta/[n*(n+1)]` for n=1,2,..., and substitute

```text
e_n = sqrt(log(2*n*(n+1)/delta)/(2*n)).
```

The sum of delta_n is delta, so with probability at least 1-delta the CDF
band holds at every sample count, threshold and subsequent receipt refinement.
This covers stopping or adding rows adaptively, provided new draws retain the
declared iid law. It is a simple logarithmic risk-spending construction, not
a claim of the tightest sequential CDF band.

If reporting only at prospectively chosen sample counts n_j, use allocations
`delta/[(j+1)*(j+2)]`, j=0,1,..., instead. The resulting radius is
`sqrt(log(2*(j+1)*(j+2)/delta)/(2*n_j))`. Within-row refinement remains free
of additional statistical charges between those reporting counts. Retained
prefix bands can be intersected to avoid losing useful earlier evidence.

## Later interval, parity and value queries

For integer a<=b, the same event implies

```text
max(0, L(b)-U(a-1)) <= P(a <= H <= b)
                         <= min(1, U(b)-L(a-1)).
```

Sum valid endpoints for disjoint intervals and clip to [0,1] for a union
bound on its probability. Every endpoint was covered simultaneously, so the
intervals or unions may be requested after seeing the data without a new
confidence allowance. Numerical width can still grow with the number of
components; simultaneous validity does not imply equal precision for every
query.

For a<b, disagreement between the SAT statuses at a and b is exactly the
event `a < H <= b`. Parity of several statuses is a union of intervals.
Thus a single threshold source covers many later graph edges and parity
questions; it does not require a separate learned distribution for each one.

A stronger, still small interface retains the feasible probability set

```text
p_h >= 0, sum_h p_h = 1,
L(k) <= sum_(h<=k) p_h <= U(k),  k=0,...,m.
```

Minimize or maximize `sum_h g(h)*p_h` to answer a bounded payoff or contrast
g(H). The true distribution lies in this set on the common event, so any
subsequently selected g is covered by the corresponding optimization. This
also enforces compatibility between interval queries instead of treating their
separate extreme values as one achievable distribution. Charge the optimization
and any policy-to-payoff compilation.

## Comparison and paid planning

For K prospectively fixed bounded events, a simultaneous two-sided Hoeffding
bound has radius `sqrt(log(2K/delta)/(2*n))`. One event can be cheaper and
sharper than constructing a full source. The DKW radius covers every threshold
without the K factor; derived interval probabilities generally use two CDF
endpoints. Compare direct event/paired-policy audits with the shared threshold
source on equal receipts and total cost, including the value of later requests.

The threshold source gives a law only after paid evidence narrows the band.
Before any useful probes its uncertainty can be almost vacuous. Large n alone
does not remove the extra width due to unresolved intervals. A useful search
policy may prioritize rows whose intervals straddle important query boundaries,
then adapt within those rows as proofs arrive. The warrant above tolerates
this acquisition policy, but does not prove it is economically optimal.

An adaptive threshold-test policy using only the observed statuses, with
fixed known query tariffs, has a payoff function g(H) and can use the common
probability set. **Real CNF proof/runtime cost is generally not a function of
H.** Different formulas can have the same transition index and very different
proof bills. Consequently the CDF band alone cannot certify lifecycle cost or
optimal paid probing. Keep measured variable costs and direct policy-payoff
calibration separate, or supply and validate an explicit joint cost model.

This source has an attractive exact structural premise: clause monotonicity
reduces each task's entire SAT-status vector to one threshold. Its prospective
benefit is a shared inference-and-proof-transfer service whose actual acquisition
cost can be compared with strong direct alternatives. No free threshold law,
solver-cost law, or confirmed material advantage is assumed.
