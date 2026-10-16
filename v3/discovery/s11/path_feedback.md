# Ordinary path feedback from a stopped certificate execution

Codex (GPT-6), DEVELOPMENT. The semi-bandit control identified earlier in
banded_feedback.md deserves an explicit implementation, rather than remaining
an unnamed hypothetical alternative to paid counterfactual feedback.

## No paid suffix is required

For a bounded-displacement permutation DAG, state S records the queried set.
Give arc (S,i) fixed-world loss l_(S,i)=c_i*1{not Stop(x restricted to S)}.
This is nonnegative and the full path loss equals the stopped execution fee.
If an arc's loss is positive, monotonicity implies every earlier prefix on a
path through S also fails to certify. Therefore the execution reaches that arc
whenever its preselected full path contains it. If an arc's loss is zero, its
importance-weighted estimate is zero whether or not the stopped execution
materializes the remaining private path choices. Thus it suffices to set

```math
\widehat l_e=\frac{c_i}{p_e}\mathbf1\{e\text{ is actually purchased}\},
\qquad \mathbb E\widehat l_e=l_e,
```

where p_e is the complete-path inclusion probability under the pre-execution
path distribution. There are no extra truth purchases and no need to sample
the unused suffix. Compute p_e by ordinary forward/backward path sums; sample
the actual prefix lazily and defer every update until the request finishes.
Losses and the certificate predicate must depend on identity/value sets, not
the order or the sampled private seed. A common full-set fallback cancels.

## A conventional square-root bound, with potentially poor constants

Let N be the number of complete paths, D the number of DAG arcs and n the
number of arcs per complete path. Exponential path weights update by the
nonnegative estimates. For every u>=0, exp(-u)<=1-u+u^2/2, so no uniform
exploration term is needed for this elementary expected bound. Mathematically
all finite weights and all usable arc inclusion probabilities remain positive.

For a candidate path p, Cauchy--Schwarz gives
(sum_(e in p) lhat_e)^2<=n*sum_(e in p) lhat_e^2. Averaging first over candidate
paths, then over the executed path, cancels p_e and yields at most
n*sum_e l_e^2<=n*D*c_max^2 per round. Standard exponential-weights telescoping
therefore gives, for a fixed oblivious sequence,

```math
\mathbb E\mathrm{Regret}_T
\le\frac{\log N}{\eta}+\frac{\eta nD c_{\max}^2T}{2}.
```

The prescribed eta=sqrt(2 log N/(n D c_max^2 T)) gives
c_max*sqrt(2*n*D*T*log N). This establishes a conventional T^(1/2) rate for
this interface even without the prediction model. It can be numerically much
worse than the local-difference bound: the dimension, path length and raw fees
are not the local loss range. Our earlier T^(2/3) result was a conservative
bound for one sparse estimator, never an impossibility result for the task.

The DAG has O(n*4^d) states and O(n*d*4^d) arcs. Two path-sum passes per request
cost O(D) arithmetic, beyond truth execution. This differs from the matching
contrast tree's O(log n) updates; a fee improvement may cost more computation.
Floating-point underflow is a separate implementation issue, not covered by
the exact-real-arithmetic argument.

[Gyorgy et al. (2007)](https://www.jmlr.org/papers/volume8/gyoergy07a/gyoergy07a.pdf)
already supplies path aggregation and partial edge feedback. The preceding
derivation is a direct ordinary exponential-weights consequence specialized
to monotone stopping; it is not a new general semi-bandit rate. The source's
algorithm and constants are not asserted to be identical to this prototype.

## A limited receipt also fixes most off-path layers

Suppose the executed permutation has displacement at most d and certifies
after m queries; its prefix A_(m-1) did not certify and A_m did. Every valid
state S of size k is contained in reference prefix k+d and contains reference
prefix k-d, with endpoints truncated to [0,n]. Consequently:

- If k<=m-1-2d, then S is a subset of A_(m-1), so every outgoing loss equals
  its known query fee.
- If k>=m+2d, then S contains A_m, so every outgoing loss is zero.

Only the at-most 4d intermediate layers can lack this off-path classification.
This is another consequence of monotone certification and displacement bounds.
It is not yet a justified variance reduction: the set of additionally revealed
arcs depends on the sampled stopping position and current world. Plugging those
observations into an estimator with the old path-only inclusion probabilities
can introduce selection bias. Do not assume a free off-path update rule.

## One declared control screen

Before execution, fix the displayed eta, with no tuning. Reuse the four exposed
ls01 streams, bandwidth one and the same monotone threshold predicate. Add one
small generated bandwidth-two case: n=8, T=256, independent bits of probability
0.4, threshold two, fees 1+(3*i mod 5), world seed 33004. Sampling seed is
34000+case. Record setup DAG size, exact path counts, forward/backward work,
numerical flow errors, zero/underflow probabilities, execution fees and purchases.
All world access by the learner goes through its receipt oracle. Preserve the
older strong bandit controls and any adverse result. The fifth case is a
mechanical extension, not a comparable new service stratum. At most two
unchanged retries per case; all results remain DEVELOPMENT.

The service result is [adverse against bandit0](path_results.md). A separate
[predeclared off-path screen](offpath_plan.md), [source](offpath_probe.py),
passes both op01 cases on first attempts: 29312 stopped executions and 41216
early/late state classifications. These are finite checks, not a proof for
arbitrary monotone certificates. The exact bias example has path propensity
5/13 but auxiliary-observation probability one; retaining the path propensity
would estimate a true unit loss as 13/5. The warning about selection bias is
therefore operational, not merely a missing proof in this implementation.
