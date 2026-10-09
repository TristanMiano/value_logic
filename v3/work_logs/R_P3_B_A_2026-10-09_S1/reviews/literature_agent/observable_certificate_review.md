# Independent review: observable purchased-label performance certificates

Contributor: **ChatGPT (GPT-6 Astra Pro)**, independent literature/semantic
review agent, October 9, 2026 UTC. Task **R-P3-B-A**, DEVELOPMENT.
Principal Research90 credit from this review and its probe: **zero**.

## 1. Verdict and exact scope

**PASS under the stated fixed-tape, predictable-forecast, positive-propensity,
action-independent policy contract.** The baseline conditional range has
width `S`, not `2S`. Its random conditional-action target is legitimate.
The binary centering extension gives one shared estimation error for the
conditional-action mean and immutable all-issued Brier score. The fixed-rate
exponential argument therefore gives their joint sampling certificate, with
no second sampling-tail allocation. Adding the independent-action tail by a
union bound gives the proposed joint terminal/Brier coverage at the fixed end.

This review covers the two prospective designs and the companion
[observable-performance derivation](../../../../derivations/07_observable_performance.md),
sections 1–6, read as 12,330 bytes with SHA-256
`e3764a72063cc16d3a61945459dee6fa8516a4abc943680459a6dc1c123c90d0`.
The design hashes and any later reviewed additive section snapshot are bound
in [the review manifest](observable_certificate_manifest.json). The separate
two-sided design and its four-tail allocation are outside this review; the
proof agent owns that extension. This is not an audit of the offline
calculator's archive-read enforcement or a new experimental result.

The exact structural probe was declared in
[the target](observable_certificate_probe_target_v1.json) before executing
[its independent checker](check_observable_certificate.py). It uses no
controller, service, archived experimental data, private evaluator or random
generator. [The complete rational results](observable_certificate_probe_result_v1.json)
retain all 32 selector paths and 512 selector/action atoms across two small
families, with 30 conditional histories and 128 prefix identity checks.
Those checks support the algebra and conditioning reconstruction; the general
confidence statement follows from the proof below, not the enumeration.

## 2. Imported methods and reconstructed application

These are established sampling and concentration tools. The contribution
being assessed is their explicit combination with this paid mathematical
feedback interface and its finite arithmetic; no method-priority claim follows.

| Source and exact locator | Import | Application reconstructed here |
| --- | --- | --- |
| D. G. Horvitz and D. J. Thompson, *A Generalization of Sampling Without Replacement From a Finite Universe*, JASA 47(260), 663–685, December 1952; [original scan](https://www.stat.cmu.edu/~brian/905-2008/papers/Horvitz-Thompson-1952-jasa.pdf), equation 6, printed p. 669, with pp. 665–667 probability distinctions | Inverse-inclusion-probability estimation of a finite total; no unrestricted optimality import | Each current block is a one-draw conditional design. Its losses may depend on past selected labels, so conditional expectations are iterated rather than pretending there is one globally fixed learned-loss population. |
| W. Hoeffding, *Probability Inequalities for Sums of Bounded Random Variables*, JASA 58(301), 13–30, 1963; DOI `10.1080/01621459.1963.10500830`; [original scan](https://www.csee.umbc.edu/~lomonaco/f08/643/hwk643/Hoeffding.pdf), section 4, Lemma 1 on printed p. 21 and equation 4.16 on p. 22 | The single-variable centered bounded-range exponential-moment inequality | Apply it conditionally to each adaptive block; no independence of block errors is imported. |
| S. R. Howard, A. Ramdas, J. McAuliffe and J. Sekhon, *Time-uniform Chernoff bounds via nonnegative supermartingales*, Probability Surveys 17, 257–317 (2020), DOI `10.1214/18-PS321`; inspected [arXiv 1808.03204v8](https://arxiv.org/pdf/1808.03204v8), submitted December 17, 2025, manuscript section 2.1, Definition 1, pp. 8–10; section 2.3, Lemma 1 and equation 2.12, p. 14 | Established fixed-rate nonnegative-supermartingale crossing framework | The finite-horizon first-crossing proof and chosen rational boundary below are supplied directly. These are version-8 locators, not journal page numbers. |

The principal's [Hoeffding inspection receipt](../hoeffding_source_inspection.json)
and [sampling-source inspection receipt](../sampling_sources_inspection.json)
record the scan hashes and actual inspected versions. This reviewer reopened
the primary URLs and checked the Howard version-8 text at the stated
definition and crossing inequality; the original scanned equation locators
rely on the principal's recorded visual inspection. No third-party PDF or
page image is redistributed in this review folder.

## 3. Filtration, chronology and the baseline certificate

Fix the complete exogenous query/answer tape, `T=mB`, and a deterministic
reciprocal-propensity envelope `S`. Use `S=B` for uniform selection and `S=2B`
for the ticket selector. Let the block filtration include the preceding
selections, settled paid answers and all allowed predictable policy data.
Before the new index `J_k` is selected, the entire current vectors `q_kt`
and `pi_kt` must be mathematically determined by that history and the fixed
tape. Their actual advance computation is a separate operational question.
The uniform implementation may issue them sequentially because they do not
change with the current selection. All `pi_kt` must be positive and must be
the actual conditional probabilities, including any adaptive allocation.

The fixed truths are constants in this mathematical probability model. This
conditioning does not make unpurchased labels available to the learner. The
probability space consists of supplied selection and action randomness, not
an IID distribution of truths and not an asserted coherent truth law `q`.

For the actual issued dyadic probability, put

```math
d_{kt}=q_{kt}+(1-2q_{kt})y_{kt},\qquad
g_{kt}=(q_{kt}-y_{kt})^2.
```

The block estimator and random target are

```math
U_k=(\pi_{kJ_k}^{-1}-1)d_{kJ_k},\qquad
V_k=\sum_{t\ne J_k}d_{kt}.
```

Their error is

```math
D_k=V_k-U_k=\sum_t d_{kt}-d_{kJ_k}/\pi_{kJ_k},
\qquad \mathbb E[D_k\mid\mathcal F_{k-1}]=0.
```

Its conditional support width is exactly the range of `d_kt/pi_kt`, bounded
by `S`, since every such value lies in `[0,S]`. The common translation
`sum_t d_kt` does not double that width. The predeclared sharp witness
`pi=(3/4,1/4), d=(0,1)` yields errors `1,-3`, with mean zero and width
exactly `4=S`.

For completeness, if a conditionally centered finite random variable `X`
has range width `c`, let `h(lambda)=log E exp(lambda X)` at the fixed
history. Its second derivative is the variance of `X` under the exponential
tilt, bounded by `c^2/4`; `h(0)=h'(0)=0`. Two integrations yield
`h(lambda)<=lambda^2 c^2/8`. This reconstructs the required single-variable
fact without applying an independent-sum theorem to dependent blocks.
Iterating conditional moments and optimizing the deterministic rate gives

```math
\Pr\{V>U+S\sqrt{m\log(1/\delta)/2}\}\le\delta.
```

Here `V=sum_k V_k` can depend on the entire selection path. A random target
causes no difficulty because the displayed difference is a martingale sum.
It is the error mean conditional on that realized selector history, not the
unconditional mean of a fresh episode, a future-generalization error or a
confidence interval for a supplied truth probability.

For `A_k=g_kJ/pi_kJ`, the identical argument estimates
`F=sum_all_issued g`. Every issued forecast is scored, including forecasts
on purchased rounds; a corrected terminal action does not erase its old
Brier loss. The baseline action-mean and Brier errors need not coincide.

Given the **entire selector/paid-feedback trajectory**, the implemented
policy's forecasts and the unbought positions are fixed. Action-independent
state, selector and bit-consumption schedules leave the unbought action bits
independent. Thus the actual terminal count `Z` is a sum of `T-m` conditionally
independent Bernoulli errors whose mean is `V`. Hoeffding's action tail can
be integrated over selection histories. Do not additionally condition on
action-dependent realized bills while retaining this conditional-distribution
argument without a separate justification.

The action-independence premise matters. In the retained finite counterexample,
`A_1` is fair but a later selector picks position zero with probability `3/4`
if `A_1=1`, and `1/4` otherwise. Conditional on that future selection,
`P(A_1=1)=3/4`. The policy could still have a different martingale proof, but
it would not inherit this full-selector-history proof.

The integer reporting radii are sound. Exactly
`sum_{j=0}^5 4^j/j! = 643/15 > 40`, so `log(40)<4`. Therefore

```math
R=S\lceil\sqrt{2m}\rceil,\qquad
r_a=\lceil\sqrt{2(T-m)}\rceil
```

dominate the two one-sided radii at error probability `1/40`. Baseline mean
and Brier each have individual coverage at least `39/40`; baseline terminal
has coverage at least `19/20`. Without using the centered identity or another
allocation, three separate tails would give only `37/40` for joint terminal
and Brier. None of these per-policy statements provides simultaneous coverage
for all 23 diagnostic arms or coverage after choosing a favorable arm.

## 4. Centering supplies one shared residual and a valid random-width bound

Binary algebra gives

```math
v_t=q_t(1-q_t),\quad r_t=d_t-\tfrac12,
\quad g_t=d_t-v_t,
\quad F-V=\sum_k d_{kJ_k}-\sum_t v_t.
```

The final difference is computable from issued forecasts and paid receipts.
The two centered estimates satisfy, pathwise,

```math
U_c=(T-m)/2+\sum_k(\pi_{kJ_k}^{-1}-1)r_{kJ_k},
\qquad A_c=T/2-\sum_t v_t+\sum_k r_{kJ_k}/\pi_{kJ_k},
```

```math
V-U_c=F-A_c=D^c
=\sum_k\left(\sum_t r_{kt}-r_{kJ_k}/\pi_{kJ_k}\right).
```

The public quantity
`C_k=max_t |1-2q_kt|/pi_kt` is predictable under the chronology above.
Each `r_kt/pi_kt` lies in `[-C_k/2,C_k/2]`, so the actual conditional
support width is at most `C_k`. Let `Q_j=sum_{k<=j} C_k^2`.
For a rate `lambda>0` chosen in advance,

```math
M_j=\exp\{\lambda D_j^c-\lambda^2 Q_j/8\}
```

is a nonnegative supermartingale. Stopping it at its first crossing of
`1/delta`, or at the finite planned `m`, proves the simultaneous sampling
boundary `D_j^c<=lambda Q_j/8+log(1/delta)/lambda` for all `j<=m`, except
on an event of probability at most `delta`. No independence of increments,
unbounded stopping limit or retrospective rate selection is required.

At `lambda=8/R` and `delta=1/40`,

```math
\rho_j=Q_j/R+R/2
```

suffices. Since `Q_m<=mS^2<=R^2/2`, `rho_m<=R`. The rate uses the
declared full horizon and deterministic envelope. Optimizing a square-root
radius using the realized random `Q_m`, or choosing a fresh favorable rate
for each prefix without correction, is not justified by this proof.

The same sampling event gives both `V<=U_c+rho_m` and `F<=A_c+rho_m`.
Combining it with the fixed-end action tail by a union bound gives

```math
\Pr\{V\le U_c+\rho_m,\ F\le A_c+\rho_m,
       Z\le U_c+\rho_m+r_a\}\ge19/20.
```

Independence **between these two events** is unnecessary. The conditional
action-randomness premise is what supplies the second event's probability.
Only the sampling component is simultaneous over block prefixes. The displayed
joint terminal statement remains fixed-end.

## 5. Clipping, exact half forecasts and limits of improvement

The public caps in the design are valid pointwise:

```math
V\le\sum_{\mathrm{unbought}}\max(q_t,1-q_t),\qquad
F\le\sum_{\mathrm{all}}\max(q_t^2,(1-q_t)^2),\qquad Z\le T-m.
```

Intersecting an upper confidence report with its matching deterministic cap
preserves its coverage. Replacing a negative upper value by zero enlarges the
reported bound and is also safe. The conditional-mean cap must not be used
as the deterministic cap for an actual count `Z`.

If every `q_t=1/2`, then `r_t=C_k=Q_j=0`, `V=(T-m)/2` and `F=T/4` exactly.
The generic fixed-rate radius still has intercept `R/2`; the exact identities
or exact caps remove that unnecessary uncertainty. Actual terminal errors
remain random, so the action tail is still needed for `Z`. At the admitted
degenerate block size `B=1`, every round is purchased and `V=Z=0`; direct
paid scoring also determines `F` exactly.

Centering does **not** always decrease a realized upper bound. Algebra gives

```math
U_c-U=\tfrac12\left(T-\sum_k\pi_{kJ_k}^{-1}\right).
```

Uniform selection makes this zero; with common clipping the centered
conditional-mean bound is then no larger because its radius is no larger.
For adaptive selection the center can move either way. Even under uniform
selection the separate Brier center can move, so a general pointwise
improvement claim would be too strong.

The prospective witness uses `B=2,m=64,pi=(3/4,1/4),q=(0,0),y=(0,1)` in
every block and selects position zero throughout. It yields `U=0`,
`U_c=64/3`, `R=48`, `rho=136/3`. The baseline clipped mean upper bound is
`48`, whereas the centered clipped bound is `64`. This path has exact
probability `(3/4)^64`; it is a counterexample to pointwise improvement,
not a confidence-level refutation. The main derivation's explicit qualifier
is therefore warranted.

## 6. Finite exact arithmetic and paid deployment boundary

Let `Q0=2^h` and write `q=a/Q0`, `d=b/Q0` with integers `0<=a,b<=Q0`.
Because `h>=1`, `r=(b-Q0/2)/Q0`; centering needs no extra denominator for
these dyadic values. Put `H=2B-1` for tickets.

| Accumulator | Uniform common denominator and numerator bound | Ticket common denominator and numerator bound |
| --- | --- | --- |
| Basic `U` | Denominator `Q0`; numerator at most `(T-m)Q0` | Denominator `(B+1)Q0`; numerator at most `m(B+1)H Q0` |
| Basic `A` | Denominator `Q0^2`; numerator at most `T Q0^2` | Denominator `(B+1)Q0^2`; numerator at most `2T(B+1)Q0^2` |
| Width sum `Q=sum C_k^2` | Denominator `Q0^2`; numerator at most `T B Q0^2` | Denominator `(B+1)^2 Q0^2`; numerator at most `4T B(B+1)^2 Q0^2` |

For a favored ticket position, `pi=(B+1)/(2B)`; otherwise `pi=1/(2B)`.
Multiplying by the stated common denominator shows the formulas directly.
For example, the `U` numerator contribution is `(B-1)b` at the favored
position and `(B+1)H b` elsewhere. The width numerator before squaring is
the maximum of `2B|Q0-2a|` at the favored position and
`2B(B+1)|Q0-2a|` elsewhere.

The controller admits `T<=8192`, `B<=1024`, `h<=32`; it uses 64-bit word
accounting. The raw unsigned numerator bounds above require at most
**45/78/88 bits** for uniform `U/A/Q`, and **57/89/110 bits** for ticket
`U/A/Q`. The integer `Q0^2` itself needs 65 bits at `h=32`. These are safe
envelope counts, not claims that every reduced sample fraction needs so many
bits. The exact cap calculation is retained in the probe result.

Centered estimates require **signed** accumulators. They use the same
denominators as their basic counterparts. Safe ticket bounds are
`-T/2<=U_c<=3T/2-m` and `-3T/4<=A_c<=3T/2`; uniform `U_c=U` and
`-T/4<=A_c<=T`. A common denominator for a centered radius and its combined
reports is `2R D_C^2`, where `D_C=Q0` uniformly and `(B+1)Q0` for tickets.
Including the factor two avoids an unnecessary assumption that `R` is even.

A deliberately loose finite envelope is also available: `D_C<2^43`,
`R<=4T<=2^15`, so that denominator is below `2^102`. The magnitude of an
estimate plus its radius and action radius is below `2^16` at the source
caps. A specifically arranged common-denominator final numerator is therefore
below `2^118`. This establishes a finite arithmetic representation. It does
not prove that arbitrary `Fraction` intermediate products stay within that
envelope, or price arithmetic, parsing, hashing, receipt checks, storage or
serialization. An executable deployment must choose and charge its actual
algorithm. No free certificate calculation is added to the saved invoices.

## 7. Primary-question value and interface obligations

This materially sharpens **Q4 within the selected finite service**. Previously
the learner-relative theorem and private evaluator told the researcher about
performance. The new interface identifies quantities the reasoner can itself
form from purchased feedback, with explicit coverage, chronology and precision
requirements. The centered version removes unnecessary sampling of the known
`q(1-q)` term and shares one uncertainty event across two useful reports.
That is a concrete operational improvement in the account of self-evaluation,
even if a resulting upper bound is loose or certifies an unattractive method.

It is not yet a proof of calibration, a prospective value-of-another-query
oracle, a guarantee of useful intervals on every episode, or a deployment
cost advantage. A valid report can be combined pathwise with an already known
resource invoice to report an upper bound on that episode's combined cost;
this does not give conditional coverage after selecting on the invoice or
identify the expected benefit of changing the policy. The ordinary exact
table comparisons and the tariff qualifications in the earlier contribution
review are unchanged.

For **Q5**, the public offset identifies a relationship between two performance
targets: knowing either target exactly, together with the permitted record,
determines the other. It does not identify all unpurchased answers or turn
fallible action probabilities into a coherent truth law. At `q=1/2`, both
performance targets are identical for any two admitted unresolved answer
assignments that agree on paid evidence. This makes the distinction concrete
whenever the admitted source actually has such remaining alternatives; hard
evidence may already fix a source coordinate independently.

The later integration interface should retain immutable issued `q`, actual
paid propensity, the purchased receipt and version, the declared horizon/rate,
the frozen-block state rule, and the randomness contract. Exact fixed-state
rounding is already reflected in the emitted `q` used here; no idealized
unrounded forecast should be substituted into the report. This concentration
statement does not itself implement the hard-state U04 update requirement.

In particular, freezing weights alone is insufficient if a future hard-answer
override changes later forecasts within a block using that block's newly
purchased answer. The direct estimator proof requires all scored `q` values
to remain predictable before the selection. A separately retained base
process may permit **upper** bounds to transfer by pointwise loss domination
when purchase/update behavior is unchanged; direct recomputation using
selection-dependent overridden `q`, or transfer of lower/two-sided bounds,
does not follow from this review. This is an integration condition, not a
defect in the presently implemented cache-free policies.

No P3-08 work, ledger/status decision, new source experiment or publication
was performed by this review. Historical P3-B and the earlier reviews are
preserved.
