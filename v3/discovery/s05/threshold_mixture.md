# A Bernoulli mixture for paid threshold calibration

Contributor: **ChatGPT (GPT-6 Astra Pro)**. October 12, 2026 UTC.
DEVELOPMENT; a precision option for [threshold calibration](threshold_calibration.md).
This adapts a standard confidence-sequence construction to retained, censored
proof receipts. It is not a new statistical method or a confirmation result.

## Scope and source actually read

Use the earlier note's iid latent thresholds `H_i in {0,...,m+1}` and sound
retained intervals `[l_i,u_i]` containing each H_i. Clause-chain probe allocation,
budgets and later revisits may adapt; all sampled rows remain in the denominator.
The population threshold law and the finite list of cuts `k=0,...,m` are fixed.
Uniform sampling with replacement from a declared finite cohort also fits.

**Howard, Ramdas, McAuliffe and Sekhon, Time-uniform, nonparametric,
nonasymptotic confidence sequences.** Read the
[primary author manuscript, arXiv v9](https://arxiv.org/pdf/1810.08240v9),
Appendix A.3, Proposition 7 and its proof, equations (56)–(57), and Section 5,
point 2. These give a two-sided beta-binomial mixture and confidence-set
inversion. The direct uniform-Beta likelihood integral below is an elementary
Bernoulli specialization of the established mixture idea, not an assertion
that the paper's tuned parameterization is identical. The manuscript itself
credits earlier Bernoulli-mixture work. Censored counts, receipt refinements and
their use in the SAT threshold interface are the application developed here.

## Complete-count confidence sequence

For a cut k, write `Y_i=1[H_i<=k]`, `q=F(k)` and `S_n=sum_(i<=n) Y_i`.
For a hypothesized `0<q<1`, mix Bernoulli likelihood ratios over a uniform
alternative parameter theta:

```text
M_n(q;s) = integral_0^1 (theta/q)^s ((1-theta)/(1-q))^(n-s) dtheta
         = B(s+1,n-s+1) / [q^s (1-q)^(n-s)].
```

For every fixed theta, the likelihood ratio at the actual S_n is a
nonnegative martingale under Bernoulli(q), starting at one. Integration
preserves this property. The maximal inequality therefore gives

```text
P_q(exists n: M_n(q;S_n) > 1/a) <= a.
C_(n,s)(a) = {q in [0,1]: M_n(q;s) <= 1/a}.
```

The event covers all sample counts; no allocation over n is needed. At q=0,
set M to `1/(n+1)` for s=0 and infinity otherwise; use the symmetric convention
at q=1. Under a true endpoint these are decreasing nonnegative processes, so
the same guarantee holds. For n=0 the confidence set is [0,1].

For n>0, log M is convex in q and minimized at s/n, where M<=1. Consequently
`C_(n,s)(a)=[L(n,s),U(n,s)]` is nonempty for `0<a<1`. Interior endpoints solve
`log M=log(1/a)` on either side of s/n. Useful exact extremes are

```text
L(n,0)=0; U(n,0)=1-(a/(n+1))^(1/n).
L(n,n)=(a/(n+1))^(1/n); U(n,n)=1.
```

Thus a fully observed zero-event cut has upper bound approximately
`log((n+1)/a)/n` when that ratio is small. This gives a practical reason to
try this option on rare threshold events.

## Why censored endpoints suffice

The two complete-count endpoints increase with s. To check this rather than
assume it, use the exact adjacent-count ratio

```text
M_n(q;s+1)/M_n(q;s) = ((s+1)/(n-s))*((1-q)/q).
q_star=(s+1)/(n+1).
```

The ratio exceeds one below q_star and is below one above q_star. For s>0,
`L(n,s)<s/n<q_star`, so at the old lower endpoint the next count's mixture
exceeds 1/a; its lower endpoint must move right. L(n,0)=0 handles the boundary.
For s+1<n, the next upper endpoint lies above `(s+1)/n>q_star`; there the
previous count's mixture exceeds 1/a, so its upper endpoint lies to the left.
U(n,n)=1 handles the other boundary.

Adjacent confidence intervals also overlap. For integer counts,
`M_n(q;s)=1/[(n+1)*P_q(Binomial(n,q)=s)]`. At q_star, counts s and s+1 are equal
modes of the binomial distribution, hence each has mass at least 1/(n+1).
Both mixture values are at most one, so q_star belongs to both intervals.

For the current proof receipts define

```text
Slo(k) = sum_i 1[u_i <= k].
Shi(k) = sum_i 1[l_i <= k].
Slo(k) <= S_n(k) <= Shi(k).
```

Reject q only if **every** compatible complete count rejects it. The accepted
set is the union of C_(n,s) over integers Slo<=s<=Shi; equivalently it accepts
q when `min_s M_n(q;s)<=1/a`. Monotone endpoints and adjacent overlap make this
union exactly

```text
[L(n,Slo(k)), U(n,Shi(k))].
```

For coverage, only inclusion of the actual complete-count set is required.
The minimum over censored counts need not itself be a martingale. The sound
receipt envelope transfers the already valid latent confidence event pathwise.

Choose positive fixed allowances a_k summing to at most alpha, for example
`a_k=alpha/(m+1)`. A union bound over cuts gives simultaneous coverage of F(k)
for **every cut, sample count and later receipt refinement**, with probability
at least 1-alpha. There is no requirement that probe censoring be independent
of H. New rows must still follow the declared iid source law.

At fixed n, improving receipts raises Slo or lowers Shi, so the band shrinks
monotonically. Use exact support values F(-1)=0 and F(m+1)=1. With equal cut
allowances both bounds are nondecreasing in k. The resulting CDF constraints
can replace the additive bounds in the earlier probability-simplex interface;
later interval, union, parity and g(H) queries inherit the same common event.
This reuse covers the fixed threshold domain; extending the source/domain or
calibrating a variable solver-cost law requires its own warranted treatment.

## Small comparison at equal total confidence allowance

[The script](threshold_mixture.py) computes the following **interval widths**.
Global alpha=.05; K=16 cuts; the mixture and per-cut Hoeffding each allocate
a=.05/16 to a cut. Complete observations have Slo=Shi. Censored rows use the
two indicated extreme counts.

| n | [Slo,Shi] | Uniform-Beta anytime | Per-cut Hoeffding anytime | DKW anytime | DKW fixed n |
|---:|:---:|---:|---:|---:|---:|
| 64 | [0,0] | .1439 | .3400 | .3065 | .1698 |
| 64 | [32,32] | .4607 | .6800 | .6129 | .3395 |
| 256 | [0,0] | .0432 | .1852 | .1699 | .0849 |
| 256 | [128,128] | .2508 | .3703 | .3398 | .1698 |
| 1024 | [0,0] | .0123 | .0996 | .0926 | .0424 |
| 1024 | [512,512] | .1321 | .1992 | .1852 | .0849 |
| 256 | [0,8] | .1021 | .2164 | .2012 | .1161 |
| 256 | [64,72] | .2533 | .4016 | .3711 | .2010 |

The comparison radii are explicit:

```text
Per-cut Hoeffding anytime: sqrt(log(2*n*(n+1)/a)/(2*n)).
DKW anytime:               sqrt(log(2*n*(n+1)/alpha)/(2*n)).
DKW fixed n:               sqrt(log(2/alpha)/(2*n)).
```

All additive intervals are clipped versions of `[Slo/n-e,Shi/n+e]`.
The two anytime additive bounds use the earlier elementary `1/[n(n+1)]`
risk-spending construction; these are not the tightest available sequential
bounds. DKW exploits ordering to avoid a cut-count penalty. Fixed-n DKW has
the narrower time scope and is plainly better at the interior counts shown.
The mixture's rare-event precision survives a moderate unresolved-count gap;
its benefit still depends on paid probes making those gaps small.

Command: `python v3/discovery/s05/threshold_mixture.py`.
[Results](threshold_mixture_results.json) retain endpoints and widths.
The run checked 4,160 adjacent-count pairs over n=1,...,64 at allowances .05
and .003125 for endpoint order and overlap, and checked the analytic zero-count
endpoint to floating error below 1e-12. These are targeted implementation
checks; the derivation supplies coverage, and no coverage simulation was run.

**Useful next choice:** try the mixture for rare cuts that control admission,
while keeping DKW as a strong source-level option. Inverting two scalar roots
per cut is a small additional computational bill; receipt acquisition remains
the potentially dominant cost. If adaptively taking the intersection or best
endpoint from both families, prospectively split alpha between them. Reporting
two alpha-level bands and selecting their narrower parts does not inherit a
single alpha guarantee for free. None of these width calculations establishes
lower total CNF proof cost or material advantage over a direct policy audit.
