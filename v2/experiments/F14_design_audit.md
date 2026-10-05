# F14 prospective design audit

Contributor: **ChatGPT (GPT-6 Astra Pro), delegated design-audit agent**.
October 4–5, 2026.
Status: **development design review; not an F15 result or independent F16 pass**.

This memo challenges the two selected F14 experiments. It reads the current
F14/F15/Gate C requirements, F04 neural design, C4 contribution assessment and
the relevant C4 recovery derivations. It does not repeat the project-wide
novelty search. The authoritative execution contract is
[`protocol.md`](protocol.md) and its frozen configuration; recommendations
below require an explicit disposition there before freezing.

## 1. Findings that affect the freeze

1. The retention challenge needs **joint feasible-source intervals and coherent
   decision regret**, not independent scalar error bars composed as if jointly
   attainable. A strong ordinary polyhedral control can reproduce those answers.
2. Rank savings, encoded storage savings, and net decision benefit are different
   outcomes. Charge retained source evidence and acquisition as well as proofs.
3. In F04's one-hidden-layer architecture, cost interchange means the selected
   units' **output contribution approximates a log cost**. Exact continuous
   cost interchange is impossible for a finite ReLU network on this domain;
   the proposed approximate test remains feasible in principle.
4. Preserving the untouched cost alone produces a donor-output target. Mixed
   pairs, equal-cost/different-factor pairs and boundary strata are necessary
   to discriminate an intermediate mechanism.
5. Cost-scale alternatives must remain a bounded, network-independent family.
   An unrestricted learned scale can turn an arbitrary output partition into
   a cost explanation by definition.
6. The selected model/alignment must be committed before evaluation. Candidate
   search on development data is not a multiplicity factor on an independent
   evaluation, but the final tested hypotheses and contrast family are.
7. Independently generated evaluation pairs permit ordinary finite-family
   concentration bounds. Reusing all Cartesian pairs, or permuting donor rows
   for a control, does not give the same independent-row sample count.

These are freeze obligations and interpretation limits. They are not reasons
to require proof reconstruction to outperform ordinary solving, or to require
a positive neural result before an honestly reported F15 can finish.

## 2. Retention: information, recovery and decisions

### 2.1 One evidence contract per comparison

For a retained linear summary `y = Bp`, let the current admissible source be

    P(y) = {p >= 0 : 1^T p = 1, Bp = y, other current source rows}.

Each method's inputs should contain its retained payload, the current request
and an explicit acquisition capability. The hidden generating law belongs only
to the scorer and to the separately declared full-information methods. An
ordinary comparator must not lose access to evidence available to the native
route. A selective method must not secretly read the original law while
choosing a bound, proof, fallback trigger or action.

The proposed three-procedure family has eight world masses with seven free
coordinates. At one old positive-penalty price profile, six order means have
rank five. A five-coordinate summary spanning that query space (implemented
as one base mean plus four residuals) and all six old means therefore make an
appropriate **equal-information** basis-versus-redundancy comparison. Singleton
marginals alone are a useful diagnostic with less information. Neither is an
equal-information competitor for an already retained complete joint law.
These dimensions follow the existing C4 derivation; this audit adds no new
rank or worldwide-priority claim.

On source withdrawal or replacement, old facts need a declared disposition.
If the challenge assumes no justified relationship to the new law, the current
source reverts to the simplex until a new fact is acquired. This is a scoped
source-change rule, not a claim that every real distribution shift destroys
all old information. Previously acquired exact facts about an unchanged source
remain available only to methods which actually retained them.

### 2.2 Three answer contracts

For a numerical query `q^T p`, use the exact attainable endpoints

    lo = min_{p in P(y)} q^T p,
    hi = max_{p in P(y)} q^T p.

If `lo = hi`, exact recovery is available. If `hi-lo <= 2*tau`, the midpoint
has worst-case absolute error at most the predeclared meaningful tolerance
`tau`. Otherwise the numeric answer is an interval or an explicit refusal
under that tolerance. Report endpoints even when returning an approximation.
The interval is information about a query, not necessarily uncertainty in an
empirically calibrated source model.

Exact rational endpoints should be compared exactly on this rational finite
challenge. Floating-point LP solutions can propose candidates, but cannot
silently supply a narrower asserted interval. Use exact checking or a declared
outward-error rule, and preserve infeasible/unresolved solver statuses.

The midpoint proof is elementary: every feasible value lies in `[lo,hi]`,
whose center is at distance at most `(hi-lo)/2`. It supplies a querywise
guarantee. Centers for several queries need not all be values of one law;
do not reinterpret the vector of midpoint estimates as recovered source data.

### 2.3 Coherent decision regret

Let `C_a(p)` be the current expected loss of an allowed action. The exact
worst-case regret of choosing `a` from the retained information is

    R(a | y) = max_{p in P(y)} [C_a(p) - min_b C_b(p)]
             = max_b max_{p in P(y)} [C_a(p) - C_b(p)].

The second expression is a finite family of ordinary linear programs. It
preserves the common law in both action costs. Subtracting separately computed
upper and lower cost bounds is a safe possible overestimate, but is not the
same exact regret and should not be presented as the strongest comparator.

The decision rule can permit `a` when `R(a|y) <= epsilon`, with deterministic
tie-breaking. Otherwise it must invoke the frozen refusal/fallback rule.
Evaluate the actual chosen action against the scorer's current law as well.
Numerical nonrecoverability need not imply a different optimal action, a large
regret, or practical harm. C4's sharp approximation witness explicitly shows
why those implications must not be imported.

A constant fallback can be included as an action if its price and residual
loss are part of `C_a`. If refusal triggers an additional fallback charge,
record that charge rather than counting the refusal as a free correct answer.
The usefulness criterion must include an informative action/answer requirement:
blanket refusal can be valid while adding no demonstrated utility.

### 2.4 Resource comparison

Record separately:

- retained original-source or summary bytes;
- proof/receipt bytes, source identities and request metadata;
- fixed shared schema/code and whether amortized or counted once;
- initial production, validation, update, replacement-search and query time;
- acquisition events and fallback events, with their declared charges;
- transient solver size or peak memory, separately from resident payload;
- final action loss/regret, refusals and failure/retry counts.

A rank-five summary is not automatically smaller in bytes than another
representation: rational numerator sizes, row descriptions and provenance can
reverse a coordinate-count advantage. A cached proof retaining the full source
must pay for both. If source acquisition has a synthetic fixed price, report
that as a scenario parameter rather than an observed real acquisition cost.

For a stationary per-update comparison, the break-even update count solves

    I_retained + u * U_retained <= I_fresh + u * U_fresh.

Include storage, checking and acquisition in the corresponding declared
cost terms before taking a ceiling. If `U_retained >= U_fresh` and initial
retention is no cheaper, there is no positive amortization advantage under
that model. Mixed revision episodes should use their actual sequence totals;
one averaged update price must not conceal adversarial repairs.

### 2.5 Native claims remain separate

An old proof can be sound for its old expression/source/request and still be
unacceptable for a new request. Conversely, a new semantic truth need not be
available to the native unit-restricted fragment. Record semantic validity,
native derivability/verification and current reception as distinct fields.
The ordinary exact comparator should receive matching unit-reachable premises
when native availability is being compared. A full-source semantic reference
is separately labeled when its information contract is broader.

## 3. Neural architecture: what subset swaps actually test

Write the network as

    h(x) = ReLU(Wx + b),
    z(x) = beta + sum_j v_j h_j(x),
    p(x) = sigmoid(z(x)).

For a coordinate subset `S`, put `phi_S(x) = sum_{j in S} v_j h_j(x)`.
Replacing that subset's base activations with donor activations gives exactly

    z^I_S(base, donor) = z(base) + phi_S(donor) - phi_S(base).

The task optimum has `z*(x) = log J0(x) - log J1(x)`. A `J0` interchange
therefore requires, on sufficiently rich base/donor support,

    phi_S(donor) - phi_S(base)
        approximately equals log J0(donor) - log J0(base).

For `J1`, the corresponding contribution is `-log J1`, up to an additive
constant. With exact base predictions and exact interchange on every pair,
these difference equalities force `phi_S = log J0 + constant` or
`phi_S = -log J1 + constant`, respectively. Fixing one anchor base proves the
statement. A raw-cost affine decoder is an auxiliary diagnostic; it is not
the quantity actually combined by this architecture's affine output.

This is a local architectural calculation, not a new causal-abstraction
theorem. Geiger et al.'s existing interchange method supplies the causal-model
comparison precedent [N1].

### 3.1 Exact obstruction and an approximate diagnostic

Every finite ReLU subset contribution is piecewise affine. On an open interval
of `c_FN`, with other inputs fixed, `log J0 = log c_FN + constant` has nonzero
second derivative. It cannot equal a finite piecewise-affine function on that
interval. Thus a zero-error continuous population criterion would be impossible
for the proposed architecture. This does **not** rule out the frozen finite
approximation criterion or useful ordinary training.

For an operational error decomposition, write

    z = z* + e,
    phi_S = log J0 + k + r

for role zero, with the symmetric negative-log expression for role one. Then

    z^I_S - z^I_H = e(base) + r(donor) - r(base).

Since the sigmoid has derivative at most `1/4`,

    |p^I_S - p^I_H|
        <= [|e(base)| + |r(donor)| + |r(base)|] / 4.

Report original prediction error and the actual interchanged probability
error. An effect-only metric may be a helpful diagnostic, but substituting
the ideal base logit for the network's base logit can hide ordinary prediction
failure and cannot be the primary causal result.

### 3.2 Pair strata

The selected five code strata answer different questions and should have
independent frozen generators:

| Stratum | Purpose |
|---|---|
| `mixed_near` | Both costs may vary; high-level intervention lies near the decision boundary. |
| `mixed_far` | Both costs may vary; high-level intervention lies away from the decision boundary. |
| `preserve_other` | Vary `J0` while holding `J1` fixed, and conversely; test specificity. Its ideal output equals the donor output, so this alone cannot establish an intermediate mechanism. |
| `equal_target` | Keep the intervened cost fixed while varying its underlying `eta` and price factors. High-level output stays at the base output; a low-level change exposes a proxy failure. |
| `scale_separating` | Mixed pairs where nonconstant scale hypotheses make meaningfully different predictions. |

For mixed pairs, ensure the distribution includes targets materially different
from both original outputs, so a whole-output transplant is actually challenged.
Define decision margins from high-level predictions before inspecting a model.
Record all selected pairs, not only originally correct or agreeable pairs.
These stratum names refer to the identity-cost high-level model. Reusing the
same pairs for a nonconstant scaled-cost hypothesis does not imply that its
own untouched cost stays fixed or its own boundary margin has the same size.

Use rejection conditions which depend only on the task generator, not model
prediction or alignment quality. Freeze rejection caps and empty-stratum
failure handling. A generator failure is not permission to lower a margin
after evaluation begins.

## 4. Cost scale and transported gauges

The bounded alternative family in this audit's first development draft was

    g(x) in {1, 1/eta(x), 1/(1-eta(x)), exp((x1+x2)/2)}.

Before the final freeze, the fourth member was replaced by
`1/(J0(x)+J1(x))`, named `inv_total_cost`. Section 11 records the reason,
geometry and limits of that choice. The exponential family and its example
below are preserved as superseded development reasoning; they are not a
fifth evaluation hypothesis.

Each family member defines `(gJ0,gJ1)` and its own interchange prediction.
A constant positive `g` is an invariant positive control, not a distinct
hypothesis. A nonconstant `g` preserves original optimum probabilities but
usually changes mixed interchanges. Fit all permitted alternative alignments
with the same development and search budget.

There is a sharp reason to forbid arbitrary neural-dependent `g`. If the base
output is exact and `S` is any hidden partition, choosing

    g(x) = exp(phi_S(x)) / J0(x)

makes `gJ0 = exp(phi_S)` and makes the complementary output contribution equal
to `-log(gJ1)` up to the output bias. Arbitrary output partitions can then be
named scaled-cost representations by construction. The predeclared small
input-function family avoids that tautology.
This argument does not guarantee that both complementary subsets satisfy
the eight-coordinate cap. Its point is that a freely chosen scale would remove
the intended content restriction, particularly for each isolated role.

For a particularly transparent scale-discrimination stratum, require
`min_g |p_H_identity-p_H_g| >= .05` over the three nonconstant alternatives.
For the superseded exponential family, this is feasible inside the original
domain: base/donor `eta=.35/.65`, with
the relevant prices one, gives identity mixed probability `.5`; the inverse
`eta`, inverse `1-eta`, and exponential alternatives give `.35`, `.65` and
approximately `.7685`. If the implemented generator instead requires only
the maximum difference to exceed a threshold, report discrimination adequacy
per rival rather than assuming all three are separated.

Report rival high-level predictions on the **same identity-aligned low-level
intervention** as well as separately searched alternative alignments if the
latter are attempted. Different alignments can legitimately realize different
decompositions. Better fit under each hypothesis's own intervention is not
unique identification of an absolute internal cost scale. If multiple families
pass, report that ambiguity. If none pass, report the bounded search null.

For positive neuron scales `a_j` and a permutation `pi`, transport incoming
weights and biases by `a_j`, outgoing weights by `1/a_j`, the subset by `pi`,
and an existing affine decoder's corresponding coefficients by `1/a_j`.
Keep its intercept unchanged. This preserves the base and swapped functions
algebraically; numerical discrepancies get a separately frozen tolerance.
Do not re-search a favorable subset after transforming the network. Report
decision ties/near-ties explicitly rather than treating roundoff-induced
threshold flips as an architectural counterexample.

Two separately successful role alignments do not establish a complete joint
two-variable abstraction. In particular, overlapping original-coordinate
subsets can prescribe conflicting values when the roles receive different
donors. A joint claim needs a compatible intervention map and tests of joint
composition/commutation; [N4] makes the non-overlapping intervention and
orthogonal-subspace requirements explicit. The small selected F14 probe can
instead report **per-role partial approximate intervention agreement**, with
overlap disclosed. It need not expand into distributed alignment search now.

## 5. Search, controls and prospective statistics

### 5.1 Match procedures, not only unit counts

All selected subsets should have the same declared size, decoder class,
development sample count and candidate-evaluation budget. A meaningful
label-guided proposal mechanism versus 128 purely uniform subsets is not an
identical search procedure. Keep uniform search as a useful additional
comparator, but also run concept-label permutation through the same proposal,
decoder fitting and ranking pipeline. Freeze treatment of duplicate candidate
subsets and zero-variance activation columns.

Use an untrained network with matched architecture and search effort, donor
correspondence controls, a deliberately decodable-but-unused fixture and a
constructed positive fixture. These controls answer different questions;
neither constructed fixture is evidence about what ordinary training learns.
Control-task selectivity has a direct primary precedent in Hewitt and Liang
[N2]; this experiment adapts the principle to a different task and adds
interchange predictions.

Training remains ordinary outcome-label weighted cross-entropy. No hidden
targets, interchange-training loss, logical supervision or architectural
modules implementing the desired costs enter the trained baseline.

### 5.2 Unit of independence

Freeze each fitted model and chosen alignment before generating evaluation
outcomes. Conditional on those fixed objects, draw independent base/donor
rows from each declared stratum. A large list of pairs made from a small pool
of shared inputs is not that many independent observations.

For a mismatched-donor control, use a fresh independently drawn wrong donor
for each row, making an independent `(base, donor, wrong_donor)` tuple.
Permuting the already-used donor rows creates cross-row dependence; the
ordinary independent-row Hoeffding calculation cannot be applied unchanged.
Different metrics or hypotheses may reuse the same pair rows: simultaneous
union bounds do not require independence **between** the metric rows.

### 5.3 Bounded loss and simultaneous intervals

Use absolute probability error `ell = |p^I-p_H|` in `[0,1]`. For a contrast
against a control on the same row, use

    Delta = ell_control - ell_candidate in [-1,1].

With family size `K`, total error budget `alpha`, and `n` independent rows,
two-sided simultaneous Hoeffding radii are

    r_abs = sqrt(log(2*K/alpha)/(2*n)),
    r_delta = sqrt(2*log(2*K/alpha)/n).

Thus an absolute-error claim uses `mean(ell)+r_abs <= tau`; a superiority
claim uses `mean(Delta)-r_delta >= delta_min`. Bernoulli disagreement or
discrimination-frequency rows use `r_abs`. Each listed statistic gets both
bounds without an additional row. Apply the classic bounded-mean theorem [N5]
and a union bound over both tails of the finite metric family; [N3], theorem 1
and corollary 2, also explicitly state the convenient bounded-mean/finite-family
forms. Clip a displayed interval to the statistic's known support.

For an equally weighted mixture of five independently generated strata with
equal `n_s`, averaging all `5*n_s` bounded observations estimates that fixed
mixture mean. Conditional means may differ across strata; the product-mgf
proof still gives the stated radius with `n=5*n_s`. This is not permission to
pool five repeated model evaluations of the same pair and multiply `n` by
five. Per-model results avoid that ambiguity.

The selected 128 development candidates do not multiply `K` when their winner
is fixed without viewing independent evaluation data. The four final `g`
families, roles, strata, controls and inferential criteria do. Five fixed
training seeds support descriptive replication of those five runs; pairwise
confidence intervals are not a confidence statement about all future seeds.

The following table preserves the **510-statistic development draft** for the
discussed five-model/four-scale/two-role design. It is **superseded by the
560-statistic cap in section 10.2**, which adds conditional base-prediction
checks. Do not use 510 for final evaluation. A final runner must emit its
actual claim table, retain its frozen cap even if fewer rows are evaluated,
and reject overflow instead of weakening confidence after seeing results.

| Statistic family | Count | Independent sample count per statistic |
|---|---:|---:|
| Per-stratum aligned absolute error: 5 models x 4 scales x 2 roles x 5 strata | 200 | 8192 |
| Candidate advantage over 4 controls, equally weighted over 5 strata: 5 x 4 x 2 x 4 | 160 | 40960 |
| Near/far disagreement: 5 x 4 x 2 x 2 | 80 | 8192 |
| Original task probability error: 5 models | 5 | Frozen task-evaluation count |
| Original task normalized decision regret: 5 models | 5 | Frozen task-evaluation count |
| Same-identity-subset scale-rival error contrasts: 5 x 2 x 3 | 30 | 8192 for `scale_separating`, or 40960 if the fixed mixture is selected |
| Per-rival high-level discrimination frequency: 5 x 2 x 3 | 30 | 8192 for `scale_separating` |
| **Total** | **510** | |

The four control names are `random`, `permuted_concept`, `shuffled_donor`
(implemented with independent wrong donors), and `untrained`. The primary
candidate arm is `aligned`. RMSE, raw decoder quality, gauge discrepancies
and overlapping subset counts can remain descriptive/finite diagnostics;
they must not acquire uncounted population claims in the report. Numerical
gauge validation also has an algebraic justification independent of sampling.

At `K=510`, `alpha=.05`, the absolute/paired radii are respectively about
`.0246104/.0492207` for 8192 independent rows and `.0110061/.0220122` for the
equal mixture of five such strata. These are prospective resolution
calculations, not observed effect sizes.

At that draft stage, the task-evaluation count, same-subset contrast population
and numerical thresholds still needed resolution; section 10 records the
subsequent specification. If development shows only that execution works,
that does not establish power for a small effect. Narrow or inconclusive
results remain an allowed F15 outcome without threshold adjustment.

## 6. Development validation and negative interpretations

F14 should validate the contract with development-only data and explicit
methodology fixtures. The high-value checks are:

- summary-fiber equality for equal-information methods; exact endpoint
  containment and coherent regret; no source-oracle access by selective paths;
- numeric exact/approximation/refusal boundaries and charged fallback paths;
- stale-source and stale-request rejection without relabeling old sound proofs;
- architecture swap identity, scalar-output transpose/index handling and
  transported gauge equality;
- decodable-unused fixture failing causal use, and positive fixture passing
  the intended intervention calculation;
- pair-stratum construction, independent wrong donors and exact score ranges;
- deterministic development execution with bounded retries, plus frozen
  configuration/seed separation and no final evaluation output.

A null speed comparison narrows efficiency claims. A correct recovery
implementation is not itself a new recovery principle. A good predictor with
poor interventions rejects its selected mechanistic explanation. Failure of a
128-candidate search is not an exhaustive impossibility proof over every subset
or every distributed representation. Decodability without causal agreement is
only correlational. Failure to learn the underlying task makes the mechanistic
probe inconclusive for that learner. Multiple successful scale families imply
limited identification. None of those outcomes automatically overturns the
separately scoped C4 synthesis/application assessment.

F15 should preserve and report these distinctions rather than redesigning the
hypothesis using its evaluation data. Specific follow-up questions can be
assigned a new prospective freeze and research chunk.

## 7. Verified primary references and review scope

Access date for the following checks: **2026-10-04 (UTC)**. No quoted passages
are reproduced. Source sections were inspected through primary PDF text or,
for the original Hoeffding theorem, the scanned page image.

**[N1]** Atticus Geiger, Hanson Lu, Thomas Icard and Christopher Potts,
*Causal Abstractions of Neural Networks*, NeurIPS 2021, pp. 9574–9586.
[Proceedings PDF](https://proceedings.neurips.cc/paper_files/paper/2021/file/4f5c422f4d49a5a807eda27434231040-Paper.pdf),
section 3, equations (1)–(3), PDF pp. 4–5; also
[arXiv manuscript](https://arxiv.org/pdf/2106.02997).
Inspected the alignment/interchange definition and the distinction from
correlational probing. Its all-interventions abstraction statement is stronger
than a finite approximate population probe. No full reproduction of its neural
experiment is claimed.

**[N2]** John Hewitt and Percy Liang, *Designing and Interpreting Probes with
Control Tasks*, EMNLP-IJCNLP 2019, pp. 2733–2743.
[Primary PDF](https://aclanthology.org/D19-1275.pdf), sections 2–3.2, especially
control-task construction and probe-capacity restrictions;
[publication record](https://aclanthology.org/D19-1275/),
DOI `10.18653/v1/D19-1275`.
Inspected these sections, not a replication. Control-task performance can
expose decoder expressivity/memorization; it does not replace causal
interventions or directly prove the required matching for our continuous task.

**[N3]** Andreas Maurer and Massimiliano Pontil, *Empirical Bernstein Bounds and
Sample Variance Penalization*, COLT 2009.
[Primary manuscript](https://arxiv.org/pdf/0907.3740), section 1, theorem 1 and
corollary 2 (PDF p. 1). Inspected its explicit bounded-iid mean inequality and
finite-family union form for the conservative calculation used here. No
empirical-Bernstein threshold, adaptive stopping theorem or variance-based
performance claim is imported.

**[N4]** Atticus Geiger, Zhengxuan Wu, Christopher Potts, Thomas Icard and Noah
D. Goodman, *Finding Alignments Between Interpretable Causal Variables and
Distributed Neural Representations*, CLeaR 2024, PMLR 236:160–187.
[Primary PDF](https://proceedings.mlr.press/v236/geiger24a/geiger24a.pdf),
sections 3.3–3.6 (definitions 1–5) and section 4. Inspected constructive
abstraction, multi-source non-overlapping interventions, orthogonal-subspace
transport and its scope. The paper's distributed search is an established
alternative to coordinate-restricted search, not an implementation added by
F14 or an uncharged fallback after a null result.

**[N5]** Wassily Hoeffding, *Probability Inequalities for Sums of Bounded
Random Variables*, JASA 58(301), 13–30 (1963), DOI
[`10.1080/01621459.1963.10500830`](https://doi.org/10.1080/01621459.1963.10500830).
Initially the original publisher/JSTOR technical text was inaccessible.
The principal agent subsequently located an
[RPI-hosted scan](https://www.cs.rpi.edu/academics/courses/spring06/random/hoefding.pdf).
This audit then visually checked original page 16 (PDF page 5), theorem 2 and
equation (2.6). The stated exponential upper-tail bound applies to independent
bounded variables without equal-distribution requirements. This is a targeted
theorem inspection, not a claim to have reread all 18 original pages.

For ordinary retention/recovery antecedents this focused audit relies on the
already documented inspection scope in
[`06_c4_contribution_comparison.md`](../literature/06_c4_contribution_comparison.md),
sections 3–4, and the actual derivations in
[`09_c4_price_revision.md`](../derivations/09_c4_price_revision.md).
No new priority claim or blanket literature-absence claim is made.

## 8. Attribution and agent timing

This delegated memo and the architectural/statistical challenge messages are
the design-audit agent's work. The retention/neural agents own their respective
implementation and contract details; the principal agent resolves the freeze
and owns the session's principal clock.

An initial UTC observation was `2026-10-04 23:18:29 UTC`; orientation and
initial source checks lacked a paired monotonic start and are **unmeasured**
here. A later paired-clock supplemental audit segment began at
`2026-10-04T23:21:10.881322+00:00`, monotonic `7138305747062` ns. The check at
`2026-10-04T23:24:30.371700+00:00` had monotonic `7337796123024` ns. These are
separate overlapping-agent observations; none is added to the principal
agent's protected F14 research floor or cumulative POST-B-1 clock.

## 9. Targeted implementation inspection and dispositions

This audit read the developing `retention.py`, `neural.py`, their focused
development tests, `calibration.py` and `F14_design_notes.md`. It did not
execute final evaluation seeds, and it does not claim a separate test run or
full code audit. The implementation observations below describe the reviewed
working tree; the principal agent owns final validation and freeze hashes.

| Concern | Reviewed disposition |
|---|---|
| Selective source access | `recover_fiber` accepts retained data, current fact status/marginals and an explicit acquisition capability. The native consistency witness is a canonical feasible vertex, not the hidden scoring law. |
| Strong exact ordinary control | Full-law methods now use `Fiber.point` and direct joint dot products; full joint moments are inverted once. They do not pay generic RREF/vertex enumeration merely to recover an already known point. |
| Conditional acquisition | The common adaptive panel first tries the retained-data criteria, then acquires only for a numeric or decision refusal. Archive bytes and calls remain charged. This fixed acceptance policy is not claimed to be an economically optimal acquisition policy. |
| Storage accounting | Durable initial cache bytes have an explicit definition; current context/proof/schema/update metadata and active serialized storage upper bounds are separate fields. Rational-cell/basis counts expose solver workspace dimensions. These are serialized sizes, not measured resident RAM. |
| Native and ordinary timing | Arithmetic-only update time is separated from complete current native production/reception time. Both need reporting; an equal native-protocol overhead is not a speed advantage over ordinary arithmetic. |
| Certificate usefulness | The updated native candidate is the certified selected order when one exists. Otherwise it is a diagnostic option. A useful-derivation candidate requires the selected-order role, a received request, a margin over fallback and at least two source premises. |
| Neural training and ranking | Training uses sampled binary outcomes only; candidate ranking prioritizes actual interchanged-probability MSE. Raw decoder quality is secondary. The focused tests poison post-hoc cost-target access during training. |
| Pair independence and discrimination | Wrong donors come from fresh streams with the same stratum donor marginal. Mixed near/far pairs challenge whole-output copying. `scale_separating` enforces the minimum difference over all three nonconstant rivals. |
| Scale and gauge reporting | All four aligned scale families have transported gauge diagnostics; same-identity-subset rival residuals and a secondary composition/commutation diagnostic are reported. Normalized original-task regret uses its sharp `11/8` range bound. |
| Constructed positive calibration | The separate compiled network uses eight ReLU coordinates per cost to approximate four univariate logarithms. Geometric secants plus the sigmoid derivative bound provide a uniform interchange-error bound. Known subsets calibrate the measurement; this is neither ordinary-training evidence nor evidence that bounded alignment search finds them. |

For the last row, each concave logarithm lies above its secant, with error at
most `(b-a)^2/(8*a^2)` on `[a,b]`. A role contains two such approximations.
The logit combines one negative approximation error and one positive error,
so its magnitude is bounded by the larger role error, rather than their sum.
This reasoning also holds for mixed base/donor costs, and multiplication by
the sigmoid Lipschitz constant `1/4` bounds probability error. The compiled
positive fixture therefore answers the earlier exact-obstruction concern by
showing a known approximate construction within the intended capacity.

The final report should retain two resource limitations: cached horizons are
model-based extrapolations from a measured update, and retention rows concern
stipulated exact source laws rather than measured empirical calibration.
Source identifiers used only for binding must not become a permitted
generator-seed lookup path to discarded data; the concrete restricted solver
does not receive or use that path.

Supplemental paired clock observations for this review were
`2026-10-04T23:28:39.561275+00:00` / `7586985700749` ns,
`2026-10-04T23:31:18.733713+00:00` / `7746158136223` ns, and
`2026-10-04T23:37:41.825075+00:00` / `8129249500306` ns.
The interval beginning at 23:28:39 contains the targeted primary-source
rechecks; the surrounding review contains derivation, design and code reading.
These supplemental spans are not a categorized principal-agent ledger and
are not added to its engaged floor. Tool waiting was not separately metered
for these agent-only observations, so no exact engaged-minute credit is
claimed from them.

Final supplemental audit observation: `2026-10-04T23:40:51.935135+00:00` /
`8319359559954` ns. The memo is ready for the principal agent's freeze integration;
it does not mark F14 or its protected floor complete.

## 10. Follow-up audit of inference and evaluation integrity

### 10.1 Scope

At the principal agent's request, this follow-up inspected the developing
`analysis.py`, `freeze.py` and `runner.py`, with targeted reads of their neural
and retention schemas. The purpose was to find concrete prospective-evaluation
failures before freezing, not to run F15 or to conduct F16's broader review.
No final discovery/evaluation seed was executed by this agent. No new source
search or separate implementation test pass is claimed in this section.

### 10.2 Final inference family: 560, superseding the 510 draft

The initial table correctly counted its listed 510 statistics, but omitted
conditional base-prediction checks. An independently sampled original-task
MAE does not bound the model's base error on a rejection-conditioned pair
stratum. A small interchange error alone therefore cannot guarantee a small
error in the intervention's **change** from its original prediction.

The refined rule adds one conditional-base MAE interval for each of five
strata and two roles, for each of five frozen models. These 50 extra rows give
**112 intervals per model and a fixed family cap of 560**:

| Statistic family | Per model | All five models | Rows per statistic |
|---|---:|---:|---:|
| Aligned interchange MAE, four scales x two roles x five strata | 40 | 200 | 8192 |
| Matched-control advantage, four scales x two roles x four controls | 32 | 160 | 40960 |
| Near/far decision disagreement, four scales x two roles x two strata | 16 | 80 | 8192 |
| Original-task MAE and normalized decision regret | 2 | 10 | 8192 |
| Same-identity-subset scale-rival advantages, three rivals x two roles | 6 | 30 | 8192 |
| Scale-separating frequency, three rivals x two roles | 6 | 30 | 8192 |
| Conditional-base MAE, two roles x five strata | 10 | 50 | 8192 |
| **Total** | **112** | **560** | |

For a row let `p_I` be the actual interchanged prediction, `p_B` the trained
network's prediction on its base, `p_H` the high-level interchanged prediction,
and `p_*` the original high-level prediction on that base. Pointwise,

    |(p_I-p_B) - (p_H-p_*)| <= |p_I-p_H| + |p_B-p_*|.

Taking conditional expectations preserves the inequality. On the simultaneous
confidence event, upper bounds of `.05` on the two means give a derived
adjusted-effect MAE bound of `.10`. No independence between those two errors
is needed. No extra statistical claim row is needed for a deterministic
consequence of the same simultaneous event. This is a mean absolute-error
bound; it does not imply a per-example guarantee or a `.10` RMSE guarantee.

The conditional-base rows from `identity/aligned` apply to every aligned `g`:
the evaluator uses the same base inputs and trained network, and positive
common cost scaling leaves `p_*` unchanged. This reuse would cease to be valid
if a future version gave each hypothesis different base pairs or a different
trained model. RMSE remains diagnostic. The `.05` probability resolution and
derived `.10` effect resolution are prospective preferences, not thresholds
fit to the development effect sizes.

With `K=560` and `alpha=.05`, the two-sided absolute/paired radii are
`.0247260580/.0494521160` at `n=8192`, and
`.0110578293/.0221156586` at `n=40960`. An observed error near `.05` consequently
cannot pass the `.05` population-mean criterion. The required confidence
margin is intentional and must not disappear when reporting the threshold.
The original-task regret interval is formed after division by the sharp
`11/8` range bound and converted back to task units for the `.05` criterion.

### 10.3 Checked analysis guards and interpretation

The inspected revision of `analysis.py` includes the following repairs:

- An exact `112 * model_count` interval-row invariant, a frozen family cap,
  and overflow rejection. Development classifications are explicitly barred
  from becoming final support.
- All four `gauges_by_g` entries are required. The guard checks finite
  nonnegative discrepancies against the frozen tolerance, a valid permutation,
  allowed positive scales and zero refits, rather than trusting a copied
  `passed` flag alone. Global-scale and unused-duplicate diagnostics are also
  checked numerically.
- Every scale-separating statistic must retain all its planned pairs, with
  `total_pairs = separating_pairs = n` and comparison count `n`. A post-hoc
  favorable subset of at least 256 pairs is insufficient.
- Conditional-base MAE and the derived adjusted-effect bound are included in
  each hypothesis's adequacy decision. Matched controls and same-subset rival
  contrasts retain the correct paired support `[-1,1]`.

The scale-separating frequency is conditional on a generator that requires
separation from all three rivals. It is one by construction when generation
succeeds. Its displayed interval must not be described as the prevalence of
separating inputs in the original input population. Rejection-generation
counts describe that construction separately.

The retention assessment uses exact finite-case classifications rather than
adding unregistered population intervals. Its useful-application criterion
requires multiple cases and source seeds, price and program revisions, and
an uncertain selective case with an accepted proof for the executed order.
It explicitly declines to infer speed superiority, unique capability or
novelty from that criterion alone. Retention refusals and their realized
fallback regret remain outcomes in the report.

### 10.4 Concrete freeze and runner obligations identified

The follow-up identified the following specific guards for the principal
agent to close before its final manifest. This table records draft findings,
not a claim that an eventual frozen revision retains each defect.

| Draft failure mode | Required prospective guard |
|---|---|
| A verified manifest could be paired with a different in-memory config. | Bind the complete supplied configuration to the manifest's committed configuration before preparation or evaluation. |
| Static import closure omitted executable parent package `__init__.py` files. | Include parent initializers and their transitive local dependencies. Include linked design documents if they supply normative details. |
| The runner verified outer checkpoint file hashes but delayed neural internal config/hash/seed/budget checks until after generating all retention evaluation cases. | Validate every prepared artifact, its internal hash, expected discovery seed, frozen config and training/search budgets before the evaluation-start marker or any evaluation generator. |
| Runtime NumPy identity was recorded without enforcing the declared pin. | Preflight the required runtime version before data exposure; preserve the actual environment in the record. |
| The run policy allowed one unchanged retry, while an exclusive start marker made retry impossible. | Provide a bounded, explicit recovery path retaining the original attempt, logs and committed preparation; never silently rediscover models or change criteria. |
| A repeated manifest-creation command could replace the anchor under the same protocol ID. | Refuse accidental overwrite or require an explicit pre-exposure replacement/version policy. A new hash is not evidence that earlier results were unseen. |
| Final retention execution bypassed `run_generated_case` while development used it. | Use the measured wrapper in F15 so common generator/source-production time is included consistently. |

An exclusive start marker in one output directory is useful but cannot prove
that no copied directory or external evaluation exists. The protocol's
pre-exposure record and honest exposure/retry ledger supply that limitation's
accountability. A native process crash can terminate before Python catches an
exception; retained start markers, partial artifacts and the process exit log
must therefore remain reviewable even without a Python failure JSON. An
unchanged bounded recovery is distinct from a deterministic code repair:
the latter requires an explicitly versioned disposition of already-exposed
cases, not an untouched-evaluation label.

### 10.5 Follow-up attribution and timing

The paired follow-up start observation was
`2026-10-04T23:45:03.819545+00:00` / `8571243970542` ns. A later observation was
`2026-10-04T23:53:03.880975+00:00` / `9051305399635` ns. These bound overlapping
agent review activity, not a principal D/L/E ledger. No part of this span is
added to the protected F14 research floor or cumulative POST-B-1 clock.

### 10.6 Subsequent static closure of the reported guards

The targeted reread on October 5 found the reported implementation guards
present in the working tree. `bound_configuration` compares the supplied
configuration with the manifest's actual configuration. The import closure
includes parent initializers; the manifest includes the normative neural and
retention design files and focused tests. Creation uses exclusive writing,
and artifact writes flush and call `fsync`.

`validate_prepared` now checks both saved networks' shapes and finiteness,
alignment identity, subset capacity and decoder correspondence, candidate
counts and selected-candidate membership, training steps, batch size, outcome
label count and zero expected-cost training labels. `_load_preparation`
checks every model and its manifest digest before the evaluation marker or
any evaluation generation. This closes the previously reported valid-hash,
reduced-training-budget loophole at the recorded-contract level.

Runtime preflight requires the pinned NumPy, CPython 3.12.x and the specified
single-thread environment. The runner uses measured retention generation.
It implements at most two explicit attempt directories, requires a concrete
unchanged-failure note for the second, preserves incomplete artifacts and
reuses complete hash-checked units. The evaluation start record now binds the
preparation manifest before exposure, and a retry must preserve that binding.
Successful stages cannot be repeated through that output directory.

This is a static closure observation, not a new execution or independent F16
pass. It does not establish global absence of prior exposure, authenticate
self-reported records against an adversary, or promise that every native
termination can produce a Python exception log. Those limits do not justify
silently discarding failed attempts. The clock observation during this reread
was `2026-10-05T00:06:01.218558+00:00` / `9828642983265` ns; no principal engaged
time is credited from it.

## 11. Fourth rival: normalized task probability

### 11.1 Selection and its reason

The final design decision replaces `exp((x1+x2)/2)` with

    g_total(x) = 1 / (J0(x)+J1(x)).

The four selected hypotheses are therefore `identity`, `inv_eta`,
`inv_one_minus_eta` and `inv_total_cost`. This keeps four hypotheses, every
matched control, the same subset/search capacity and the 560-statistic family.
The choice follows the explanatory question before final evaluation; it is
not a selection based on trained-network performance against these rivals.
Earlier exponential-family artifacts remain development artifacts with their
original identities.

Writing `q(x)=p_*(x)=J0(x)/(J0(x)+J1(x))`, the new costs are `(q,1-q)`.
This is a direct ordinary competing explanation: the network may organize
information around the prediction required by its training objective rather
than around absolute expected action costs. Here `q` is the optimum prediction
for weighted cross-entropy; it is not generally the outcome probability
`eta`. The existing inverse-`eta` rivals instead test assignments that make
one role a raw false-negative or false-positive price input.

The exponential rival was useful because its log scale is an affine function
of the raw inputs. It demonstrates the freedom to cancel an arbitrary term
between the two output contributions. The unrestricted-scale argument in
section 4 already explains that limitation. Within a four-member budget,
normalized task probability supplies a more direct ordinary interpretation
to challenge. This is a reasoned choice of comparator, not a claim that it is
the universally strongest alternative for every shallow network.

### 11.2 Interventions, geometry and capacity limits

For base `b` and donor `d`, the normalized rival predicts

    role 0: q(d) / (q(d)+1-q(b)),
    role 1: q(b) / (q(b)+1-q(d)).

The original and normalized predictions coincide for these positive costs
exactly when the base and donor total costs agree. Thus variation in total
cost challenges this rival even when observational predictions do not. The
normalized coordinates sum to one observationally, but a one-role
intervention deliberately replaces one structural assignment; its mixed
denominator need not remain one. The comparison is an intervention on this
specified two-coordinate high-level model, not evidence that the ordinary
training objective identified it uniquely.

An analytic development witness shows that separation from all three rivals
is feasible simultaneously. Let the base have `eta=1/3`, prices `(1,1/2)` and
therefore `J=(1/3,1/3)`. Let the donor have `eta=2/3`, prices `(2,2)` and
therefore `J=(4/3,2/3)`. Their original predictions are `1/2` and `2/3`.

| Intervention | Identity | Inverse eta | Inverse one-minus-eta | Inverse total cost |
|---|---:|---:|---:|---:|
| Replace role 0 | 4/5 | 2/3 | 8/9 | 4/7 |
| Replace role 1 | 1/3 | 1/2 | 1/5 | 3/5 |

Every rival differs from identity by more than `.05`, and both original
interchange predictions differ from the original base/donor predictions by
the mixed-pair cutoffs. The inequalities are strict, so nearby interior
inputs also satisfy them even though the displayed price witness uses domain
boundaries. This is a constructed development argument, not a held-out case,
an estimate of rejection-sampling efficiency or a trained-model result. The
new generator still needs its separate development execution check.

Equal subset size and search budget do not imply equal approximation
difficulty. Under the affine-output derivation, normalized role contributions
must approximate

    log q = log J0 - log(J0+J1),
    -log(1-q) = -log J1 + log(J0+J1).

The log-sum term couples the raw outcome and price inputs. It may be harder
for the fixed shallow, eight-coordinate subsets than the exponential rival's
affine cancellation term. No extra capacity or post-evaluation search is
authorized to compensate. A failed separately fitted normalized arm would
reject its stipulated bounded realization; it would not refute every
normalized-probability explanation.

The same-identity-subset rival comparison is therefore essential: it asks
which high-level prediction fits the **same observed low-level intervention**,
without requiring a normalized alignment search to succeed. Even a decisive
result there concerns the selected partial intervention and bounded rival
family. Another subset could support another decomposition. A positive
result still cannot establish a unique absolute cost scale or a joint
constructive abstraction. Had normalized probability been excluded, that
exclusion would have been a material named limitation of the tested family;
the explicit partial scope would have remained logically possible but less
informative about this direct alternative.
