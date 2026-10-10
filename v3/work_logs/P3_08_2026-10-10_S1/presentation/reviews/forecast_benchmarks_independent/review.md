> **Portable display copy — notation only.**
>
> Original: [v3/work_logs/P3_08_2026-10-10_S1/reviews/forecast_benchmarks_independent/review.md](../../../reviews/forecast_benchmarks_independent/review.md)  
> Original SHA-256: `27af2cd6aeef31e57cd4f232e2136738ab73f145634f37ab8ca460026714f281`.
>
> Generated with the unchanged math guard's `transform(protect=True)`,
> plus relocation of relative links to their original destinations.
> The original scientific document remains unchanged. This is a source-notation
> check, with no live-render or new mathematical validation claim.

# Independent forecast benchmark review — DEVELOPMENT

Contributor/model: **ChatGPT (GPT-6 Astra Pro)**, 2026-10-10 UTC.
Same-model, nonblind post-score review. **Zero principal time credit.** Private
truth reads were authorized for this audit; the earlier public-only reporter
reviews remain closed and unchanged.

**Pass for the exact sealed scope.** I found no score-formula, dyadic-rounding,
preissue-hard-mask or record-membership defect in the inspected v2 benchmark.
The independent checker reconstructed every field of all 63 saved broker
benchmark rows from the sealed public records and private truth. It also
reconstructed their 5,376 forecast positions, checked every public record hash,
and independently agreed with the earlier private base/live Brier totals.
No producer, broker, reporter, policy or private truth evaluator was executed.

The appropriate compact presentation uses **18 scenario/selector/seed
configurations**, with hard mode shown separately. These configurations are
also not independent statistical trials: there are three fixed public tapes,
two selectors and three deterministic development seeds, all already exposed
before this post-score analysis.

## Compact results

Each cell is **strictly better / equal / strictly worse**, comparing Brier
totals on the same complete tape. Every row covers the same 18 configurations.
The static-mixture comparator is evaluated both exactly and on the broker's
initial dyadic grid; their signs agree here, although their exact totals differ.

| Forecast and information history | Constant half | Hindsight best single fixed expert | Static equal mixture, exact | Static equal mixture, dyadic |
| --- | ---: | ---: | ---: | ---: |
| Immutable base forecast, all positions | 18 / 0 / 0 | 6 / 0 / 12 | 18 / 0 / 0 | 18 / 0 / 0 |
| Live forecast, hard off | 18 / 0 / 0 | 6 / 0 / 12 | 18 / 0 / 0 | 18 / 0 / 0 |
| Live forecast, hard on; every comparator receives the same preissue hard answers | 17 / 0 / 1 | 7 / 0 / 11 | 11 / 0 / 7 | 11 / 0 / 7 |

The base forecast beats the best individual binary expert on the six
`repeat_online` configurations and loses on the twelve `cold_mixed` and
`cheap_structure` configurations. After matching hard history, the live
forecast also beats the best matched expert on `cold_mixed/uniform/seed11`.

The seven adverse live/static comparisons are **all six `cheap_structure`
configurations and `repeat_online/uniform/seed11`**. The sole adverse
live/half comparison is `cheap_structure/uniform/seed29`: 48 of its 64 answers
were already hard before issuance, leaving 16 unresolved issue positions.
Its live Brier total is exactly `12227338737/2147483648` (about 5.693798),
versus 4 for the matched half forecast and `44/9` (about 4.888889) for the
matched exact static mixture. The live score is smaller than that episode's
base score, but the same hard corrections improve the comparators enough to
make these matched comparisons adverse.

For `repeat_online/uniform/seed11`, the live total is about 15.051471 while
the matched static exact total is `521/36` (about 14.472222). This case still
beats the matched half forecast and the best matched binary expert. Neither
the favorable nor adverse comparisons were dropped.

The 63 stored rows contain four variants per uniform configuration and three
per ticket configuration. The additional variants change hard-state indexing
or the selected exact solver. I verified identical base forecasts, advice,
selected positions/labels and actual propensities within every configuration;
I separately verified identical scores within each fixed hard mode. Thus the
archive consists of 27 hard-off rows and 36 hard-on rows, with duplicate
implementations retained for provenance. The raw result counts are correct,
but they weight uniform configurations four times and ticket configurations
three times and must not be presented as 63 independent trials.

## Independent formulas and chronology

Let $`y_t\in\{0,1\}`$ be sealed evaluator truth, $`q_t`$ the immutable base
forecast, and $`H_t`$ indicate that a successful, checked, current full-key
receipt was already retained **before** issue $`t`$. The actual live forecast is

```math
q_t^{\rm live}=(1-H_t)q_t+H_ty_t.
```

For any comparator forecast $`p_t`$, the matched comparator is
$`p_t^H=(1-H_t)p_t+H_ty_t`$, so its Brier total is

```math
\sum_t(p_t^H-y_t)^2=\sum_t(1-H_t)(p_t-y_t)^2.
```

The half comparator therefore has total $`T/4`$ before matching and
$`(T-\sum_tH_t)/4`$ after matching. A fixed binary expert has total
$`\sum_t\mathbf1\{a_{tj}\ne y_t\}`$, or the corresponding sum over
$`H_t=0`$. The best fixed expert is the minimum of these **six whole-tape
totals**, with tied minimizers preserved in the independent diagnostics. It
is not a per-position hindsight switch among experts. Matching history can
change which whole-tape expert minimizes the score.

The checker forms $`H_t`$ from the prior selected receipt sequence, validates
request identity, full key, scope, successful/checked status, provider and
provider version, and only then checks the archived `hard_before` value. It
adds the current selected receipt after checking the issued forecast. Thus a
newly purchased answer at $`t`$ does not retroactively improve that issue's
forecast score; it may improve later issues of the same claim. These archived
episodes have fixed hard mode, no withdrawal, generation change or conflict,
and a sufficient hard-store capacity. The terminal store counts also agree.

All six advice values were independently reconstructed from the public CNF
features using sets/counts, without importing the deployed expert function.
The archived expert-name tuple matches the benchmark dictionary order. Public
query IDs and complete keys match the sealed input tape at every position.
The checker evaluates Brier totals through the binary quadratic expansion
$`\sum_t(p_t^2-2p_ty_t+y_t)`$ using exact `Fraction` arithmetic, without
importing the benchmark calculator.

## Why the static dyadic comparator is exact for this broker

Write $`k_t=\sum_{j=1}^6a_{tj}`$, $`D=2^{\texttt{action\_bits}}`$ and
$`W=2^{\texttt{state\_bits}}`$. The archived `NumericProd` constructor gives
every expert exactly weight $`W`$. Its prediction numerator is

```math
\left\lfloor\frac{D\sum_jWa_{tj}}{\sum_jW}\right\rfloor
=\left\lfloor\frac{Dk_t}{6}\right\rfloor.
```

Hence the exact static comparator is $`k_t/6`$, and the static executing-grid
comparator is $`D^{-1}\lfloor Dk_t/6\rfloor`$. This uses the **action precision**;
it does not assume that rounding the normalized expert weights produces an
exact uniform probability vector. The broker initializes equal unnormalized
weights, so no such assumption is needed.

The benchmark uses the raw `base_q[1]`. That would be insufficient if the
stored fractions had varying reduced denominators, but the archived broker
stores the unreduced pair `[numerator, 2**action_bits]`. I checked all 5,376
denominators: each is 65,536. Every first-block base prediction exactly equals
the independent static dyadic prediction, and every later base numerator
agrees with its stored block-entry weights. The truncation error lies in
$`[0,1/D)`$ at every position. There is no nearest-rounding substitution.

## Interpretation and remaining limits

The v2 amendment is appropriately prospective **for its additional
calculation**, following exposure to v1 scores. It explicitly adds the static
mixture because beating binary constituents alone does not isolate adaptive
weighting. The resulting observed base-score improvement over this static
mixture is a useful descriptive fact about these tapes and selected-label
histories. It is not a frozen unseen challenge or a prospective generalization
result.

The matched benchmarks inherit the episode's hard history. They do not run
their own acquisition rules, change the selector's favorites, or regenerate
selected labels. In particular, substituting a static forecast into a ticket
selector could change its selected-query distribution. These saved-score
comparisons deliberately do not assert that counterfactual deployment.

Brier loss is a forecast score. The expected error of a Bernoulli terminal
action depends linearly on the forecast, and selected purchases/hard answers
can further change terminal actions. Consequently a smaller Brier total does
not itself establish a smaller realized terminal error or a smaller
`terminal errors + price * charged units` objective. No new setup, forecast,
acquisition, reporting or retained-history invoice was constructed for these
diagnostic comparators. The hindsight best expert and free perfect-truth
reference are not charged deployable controls. The main paid ordinary
catalogue and ordinary-kernel equality claims therefore remain separate.

No IID, calibration, confidence-coverage or universal learning claim follows
from these 18 configurations. The existing analysis contract and v2 amendment
state these distinctions correctly. No production change is recommended.

## Source binding and reproducibility

| Item | SHA-256 |
| --- | --- |
| Current and saved v2 benchmark source, 7,258 bytes | `1e67719034046612bf10b1043f4e720a77ee588e9321e60caf9a462fec67e934` |
| Analysis contract | `ae57be88330ace9ececc8505628e4b2f002bba20a86606c45b8f6c70975618fb` |
| v2 amendment | `08ed4989cb44de38cc9a365bc774c3f746dd9b6e2b4933506f00e4f10b825c4a` |
| Saved v2 benchmark results | `01f0ca20d3112ffd40cd78818898ec86175ca829f75c91b56bf83c1d140e72df` |
| Archived broker v1.2 | `248642e00333f0939f2e0e41020c69879b2d5bcedacf7979f980583630ba3653` |
| Independent checker | `2cf1189222ff6beee1a991af6b128945a43d649a9185de03eaae486cf9093366` |
| Independent results | `73d092ffd4053184707a64ced59050dd926bd898e00b8be8a16cb38a92dc763c` |

The complete input/source inventory is `run_v1/input_manifest_before.json`;
its hash is
`8099f428ef4d66a3380182f5827c991849a296dacc37aca0660c0a6901790085`.
Its after-manifest is identical. All seven public seal entries, both private
seal entries, the private truth's binding to the public seal, all 186 public
record hashes and exact broker membership were checked. All eleven archived
policy source files match their source-before and source-after entries; their
copies and the benchmark source are retained under `run_v1/source/`.

`run_v1/results.json` retains exact reconstructed rows, the full 18-entry
configuration table, adverse cases, tied best expert names and all check
counts. The check count is an implementation-verification count, not a sample
size. The complete checker ran once and passed; it added zero policy runs.
To reproduce the arithmetic from the same repository root, use a fresh output
directory:

```bash
python v3/work_logs/P3_08_2026-10-10_S1/reviews/forecast_benchmarks_independent/audit.py --out v3/work_logs/P3_08_2026-10-10_S1/reviews/forecast_benchmarks_independent/reproduction
```
