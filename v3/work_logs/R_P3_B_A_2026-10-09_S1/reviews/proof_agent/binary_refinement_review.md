# Independent review of exact-log, rate and precision refinements

Contributor: ChatGPT (GPT-6 Astra Pro), 2026-10-09 UTC. R-P3-B-A.
Same-model, nonblind independent mathematical reconstruction and exact
arithmetic review. **Zero principal research-clock credit.** No policy was
changed or newly executed; no P3-08 integration was started.

## Verdict and source boundary

**PASS.** The exact-log comparator coefficient tightens the guarantee for
the already executed uniform rule, including its existing fixed-state
allowance. The 20 saved refined certificates correctly preserve the policy,
data, seeds and source version. The two faster-rate derivations are valid
mathematical options; their runtime cost and observed performance have not
been established by the unchanged-policy evidence. The finite-precision
lower bound is valid, with the two lower floors combined by a **maximum**,
not by adding them.

| Reviewed document or program | SHA-256 |
| --- | --- |
| `development/binary_potential_refinement.md` | `e4cf3be0d5c98d47bc1fd0ebbdb34d6c03a5d3d15b3a77d92517b660c76d2d52` |
| `development/deployment_bound_design.md` | `48721d24153850fb440e70cd525499f64c5b60a62a388dd463ec6a849728aa6c` |
| `development/binary_potential_certificates.py` | `ade39f444fa9d2e025de6f26e98533878b9bcb5ad8593cf8f4296db3663d4516` |
| `development/binary_potential_certificates.json` | `f13df1ca31517af76bbd49c58556e3222145055e4a43490401c1143eba85a1c4` |
| Certificate input `development/service_comparison/run_001/result.json` | `a99010afcd0667f6f8c6cbfa4588853333b80a24151b6e95a4aa3249d7c444b1` |

The reviewed copies are saved in this review directory, preserving the
documents' exact wording at review. The first unrounded exact-log alternative
already appears in this reviewer's initial `review.md`, §2. This later note
checks the fixed-state integration, new numerical certificates and rate and
precision consequences; it does not claim the potential identity as a new
discovery.

## 1. Exact comparator log and fixed-state telescope

For block losses `x_{ki}` in `[0,1]`, let the normalized product update have
learning rate `0<eta<1`. Put `mu_k=sum_i p_{ki} x_{ki}`. With exact state,

`p_{k+1,i}=p_{ki}(1-eta*x_{ki})/(1-eta*mu_k)`.

The fixed-mass floor-plus-one implementation instead guarantees

`p_{k+1,i} >= (1-delta) p_{ki}(1-eta*x_{ki})/(1-eta*mu_k)`,

where `delta=2^-s`. Start from `p_{1i}=1/N`, take logarithms and telescope.
Since `p_{m+1,i}<=1` and `log(1-eta*mu_k)<=-eta*mu_k`,

`eta sum_k mu_k <= log N - sum_k log(1-eta*x_{ki})
                       + m log(1/(1-delta))`.

For binary selected expert losses,
`log(1-eta*x_{ki})=x_{ki} log(1-eta)` exactly. Therefore

`sum mu_k <= beta(eta) sum x_{ki} + log N/eta
              + m log(1/(1-delta))/eta`,

with `beta(eta)=-log(1-eta)/eta`. The term containing `delta` is zero in exact
state. The same upper bound is valid for fractional losses because concavity
gives `log(1-eta*x)>=x log(1-eta)` on `[0,1]`; only the binary log term is
an equality. The final loss theorem still contains other inequalities.

In the uniform-block service the loss tape is fixed, expert actions are
fixed public functions of requests, and the fresh uniform selected index is
independent of the current block's frozen weights. Thus expected selected
loss of a fixed expert is `L_i/B`, and the ideal unbought mixture loss is
`(B-1)` times expected selected mixture loss. The full-tape minimizer is
deterministic, so it may be selected as this fixed comparator before taking
the expectation. There is no exchange of expectation with a random hindsight
minimum.

The resulting bound is

`E terminal_loss <= [(B-1)/B] beta(eta) L*
                     + (B-1) log N/eta
                     + (B-1)m log(1/(1-2^-s))/eta
                     + (T-m)2^-h`.

The dyadic action term can be dropped when an independently proved exact
grid condition applies. Under the executed `eta=1/K`,

`alpha_exact = ((B-1)/B) K log(K/(K-1))`.

The normalization allowance may retain its old safe rational upper bound
`(B-1)mK/(2^s-1)`. The log-`N` term and tariff records are unchanged.

For `eta<=1/2`, the positive log series gives

`-log(1-eta) < eta + eta^2/[2(1-eta)] <= eta+eta^2`.

Hence `beta(1/K)<1+1/K`. For admitted `B>=2`, `K=max(2,B-1)` and the
old coefficient `((B-1)/B)(1+1/K)` is at most one. The exact-log coefficient
is strictly smaller. The old `B=2` coefficient `3/4`, for example, becomes
`log 2`; no executed action or receipt changes to obtain that improvement.

The all-issued uniform Brier certificate follows from the separate uniform
full-mixture bridge and convexity:

`E sum Brier(q_t,y_t) <= beta(eta)L* + B log N/eta
                         + Bm log(1/(1-2^-s))/eta + 2T2^-h`,

clipped at `T`. This is the formula used by the refined certificate program.
It does not pretend that buying an answer retrospectively corrects the
pre-issued scalar forecast.

## 2. Independent audit of all 20 saved certificates

The root program uses the positive atanh expansion

`log(a/b)=2 sum_{j>=0} z^(2j+1)/(2j+1)`, `z=(a-b)/(a+b)`.

After 24 terms it bounds the tail by
`2 z^49/[49(1-z^2)]`. This is a sound rational enclosure: each remaining
denominator is at least 49, leaving a geometric series in `z^2`.

To avoid merely copying that implementation, the independent check uses

`log(K/(K-1)) = sum_{j>=1} (1/K)^j/j`.

After 128 terms its upper tail is
`(1/K)^129/[129(1-1/K)]`. Every saved log enclosure strictly contains this
independently computed narrower interval, including `log 2` used to enclose
`log 4`. All operations and comparisons use exact `Fraction` arithmetic.

The check verifies the input and program hashes and every one of the 20
saved uniform rows: old and new comparator coefficients, private full-tape
`L*`, source-known `T/2`, fixed-state and action allowances, unclipped
arithmetic followed by the correct hard clipping, Brier allowance, bound
reduction, displayed decimal conversion, and preservation of source version
and `policy_change=False`. Every refined terminal certificate is at most
its original saved terminal certificate.

For the saved `T=3968`, `B=8`, `s=h=16` main arm, the refined expected
terminal-loss upper bound is approximately **1820.7371857549495** using the
private retrospective `L*`. Its source-known expected upper bound is
approximately **1941.59131873952** using `L*<=T/2`. The rigorous bounds are
the rational strings in the saved certificate; these decimal figures are
displays of those numbers, not observed loss or pathwise limits.

This validation is a mathematical calculation over existing evidence. It
adds zero policy executions and does not choose among rates or seeds by
observed performance.

## 3. Uniform faster-rate candidate: correct but unexecuted

For every `0<eta<1`, the positive power series yields

`-log(1-eta) <= eta + eta^2/[2(1-eta)]`.

Choose `eta=2/(B+1)` for `B>=2`. Then

`((B-1)/B)[1+eta/(2(1-eta))]=1`.

The uniform exact-log theorem therefore implies a comparator coefficient
at most one, with log allowance

`(B-1)/eta * log N = (B^2-1) log N/2`

and fixed-state allowance at most
`(B^2-1)m/[2(2^s-1)]`. Exact integer update factors could be `B+1` for a
correct expert and `B-1` for a wrong expert. Both are positive, including
the `B=2` case where the rate is `2/3`. The earlier quadratic approximation
requiring `eta<=1/2` cannot justify that case, but the present logarithmic
bound can.

For `B>=4`, the coefficient of `log N` is smaller than the executed
conservative `(B-1)^2`. This does not establish uniform superiority of the
entire certificate: the executed exact-log theorem retains a first-order
coefficient below one, and all finite terms and actual costs matter. At
`B=2`, in particular, the older rate can yield the more useful first-order
term when `L*>0`.

The independent calculation confirms all ten saved power-of-two `B` rows,
their rates, integer factors, exact coefficient caps and log allowances.
These rows are correctly labeled **unexecuted mathematical options**.
Changing the source or interpreting old samples as if generated at this rate
would require new prospective admission and evidence. No such change occurs
in this review.

## 4. General probability-floor candidate, including adaptive tickets

The extension beyond binary selected updates is also valid. For
`0<=u<=eta<1`,

`-log(1-u) <= u+u^2/[2(1-eta)]`.

This follows by bounding `1/j<=1/2` for all powers `j>=2`, summing the
geometric tail in `u`, and using `1-u>=1-eta`. Apply it to `u=eta Z_i`,
where `Z_i=X_i/H` and `0<=X_i<=H`. The potential gives

`sum p dot X <= sum X_i + H log N/eta
                + eta/[2H(1-eta)] sum X_i^2`

plus `Hm log(1/(1-2^-s))/eta` in fixed state.

For the adaptive remaining-action estimator
`X_i=(1/pi_J-1)ell_{Ji}`, the conditional coefficient of each binary
comparator loss is

`1-pi + eta(1-pi)^2/[2H(1-eta)pi]`.

Since `(1-pi)/pi<=H`, this is at most one whenever
`eta H/[2(1-eta)]<=1`. Equality at `eta=2/(H+2)` supplies the safe rate,
log allowance `H(H+2)log N/2`, and fixed-state allowance
`H(H+2)m/[2(2^s-1)]`. The same inequality extends to losses in `[0,1]`
by replacing `ell^2` with the upper bound `ell`.

For uniform sampling `H=B-1`, this recovers the uniform candidate above.
For the executed ticket *distribution*, `H=2B-1`, a hypothetical new-rate
update would have

`gamma_nonfavorite=2/(2B+1)` and
`gamma_favorite=2(B-1)/[(B+1)(2B-1)(2B+1)]`.

The hypothetical common denominator is
`(B+1)(4B^2-1)=4B^3+4B^2-B-1`. At `B=1024` it equals
**4,299,160,575**, which needs **33 bits**. The executed denominator
**4,294,964,225** needs 32 bits. Both fit a 64-bit word, but the existing
source-specific denominator assertion and working-bit formula must not be
reused unchanged for a different implementation. Actual new normalization
and factor arithmetic would need its own capacity and cost review.

The independent rational check confirms the comparator inequality and the
denominator formulas for each admitted power-of-two block size. It runs no
adaptive policy at the hypothetical new rate and makes no performance-price
claim for that candidate.

## 5. Source-known bounds and finite precision

The source's constant-zero and constant-one experts have losses summing to
`T` on every binary tape. Therefore `L*<=T/2` is a certified source property,
not a paid evaluation of the mathematical answers. It may be substituted
into a theorem with a nonnegative comparator coefficient. A sharper private
`L*` stays a retrospective certificate input unless the additional evidence
is admitted and paid. Expected terminal bounds can be clipped at `T-m`;
pathwise spending remains governed by its separate hard funded cap.

For `A=(B-1)mK` in the executed uniform rule or `A=HmK` in the adaptive rule,
choosing `2^s>=1+A/epsilon_s` gives `A/(2^s-1)<=epsilon_s`. Choosing
`2^h>=(T-m)/epsilon_h` gives action allowance at most `epsilon_h`.
Integer ceilings should implement these inequalities directly; the
executable `1<=s,h<=32` limits remain binding. At `N=4`, fixed total mass
is `2^(s+2)`, so `h>=s+2` makes every mixture probability exactly representable
on the action grid. This removes the *action-rounding allowance*, while
finite normalization and the cost of the action bits remain.

The lower-floor construction supplies the complementary warning. Consider
an all-true request tape. The library contains a constantly wrong zero
expert. Positive product factors keep its weight strictly positive forever;
fixed-mass normalization also keeps every weight at least one. Thus the
unrounded probability `p_t` of answer one is strictly less than one at every
finite round. Downward rounding implies

`q_t <= 1-2^-h`.

Condition on any selected-index and past-feedback history under the fair-bit
model. Each unbought action then errs with probability at least `2^-h`.
There are exactly `T-m` such positions, yielding

`E terminal_loss >= (T-m)2^-h`, even when `L*=0`.

With fixed total mass `M`, the wrong constant's share is at least `1/M`.
Downward rounding cannot increase the correct-action probability, so also

`E terminal_loss >= (T-m)/M`.

Combining these statements yields

`E terminal_loss >= (T-m) max(2^-h,1/M)`.

The two terms must not be summed: they lower-bound the same error. The
strongest simple bound here is their maximum. A valid source request is
`p=17,a=1`, whose Euler equality is true and whose four public expert actions
are `(0,1,1,1)`. Repeating that input realizes the premise without an
empirical search for a difficult tape.

At fixed `h` and `s`, these floors grow with the number of unbought positions.
The asymptotic statement concerns a growing family of admitted mathematical
contracts; the current executable still rejects `T>8192`. It prevents
unqualified constant-in-horizon regret language for a fixed-precision
implementation. It also identifies a precise possible P3-08 integration
benefit: a sound retained-answer override can correct this repeated known
answer while retaining the raw learner's update as a separate component.
That is an integration boundary and future question, not work started here.

## 6. Forecast and action baselines: objective boundary

The deployment design's diagnostic baselines are valid. A fixed scalar
forecast `q=1/2` has Brier loss exactly `1/4` for either binary answer, so its
all-issued score is exactly `T/4`. For any fixed selection path, independent
fair-coin unbought actions have expected terminal mistake count `(T-m)/2`.
Neither fact implies that a fractional Brier baseline is the same decision
objective as a sampled terminal action. These were analytic diagnostics
after the runs, not new prospectively deployed comparison arms.

The conditional valuation identity is also correct under its stated extra
premises. If there is an external subjective truth probability `p` and an
independent action lottery with probability `q` of answer one, expected
zero-one loss is `q+(1-2q)p`. With independent correction probability `pi`
and known stake `c>0`, its variable paid-loss contribution is
`c(1-pi)[q+(1-2q)p]`. At `q=1/2` or `pi=1`, this is independent of `p` and
cannot identify it. This conditional algebra is not a probability law for
the mathematical inputs, nor does a regret upper bound become a point
estimate of subjective truth.

## Supporting evidence

`binary_refinement_probe.py` and its saved stdout JSON verify every relevant
certificate field with independent log enclosures; stderr is empty. The
manifest binds the reviewed notes, certificate program, certificate JSON,
probe and output. All 20 unchanged-policy certificates and all ten saved
uniform rate options pass. The adaptive candidate arithmetic was checked
separately across the same ten block sizes. No new policy, empirical arm,
source version, source-price relabeling or clock credit was introduced.
