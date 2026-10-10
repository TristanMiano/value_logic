> **Portable display copy — notation only.**
>
> Original: [v3/work_logs/P3_08_2026-10-10_S1/reviews/price_envelope/review.md](../../../reviews/price_envelope/review.md)  
> Original SHA-256: `afc2e89e570c088d107c70cd9fb43472617b849fe89ef35e6b91e0d6bae53bc9`.
>
> Generated with the unchanged math guard's `transform(protect=True)`,
> plus relocation of relative links to their original destinations.
> The original scientific document remains unchanged. This is a source-notation
> check, with no live-render or new mathematical validation claim.

# Exact fixed-transcript price envelope: independent review

Contributor/model: **ChatGPT (GPT-6 Astra Pro)**, integration reconstruction reviewer.
Written **2026-10-10T17:45:51.763132+00:00**. **P3-08 DEVELOPMENT; same-model, nonblind, read-only review.**
The reviewer had already read development scores. Principal research credit is
**zero seconds**; no overlapping or historical time is added. This work executes
an offline evidence checker only. It edits no policy, regenerates no query or
truth, and runs no policy or reporter. No P3-09, contribution, or advancement
decision is made.

## Disposition

**PASS for the exact frozen 234-record catalogue.** There is no discrepancy in
the line parameters, eligibility, pairwise rational intervals, coincident lines,
closed endpoints, displayed intermediate-price winners, or stated source transfer.
The interpretation limits in the declared analysis contract are necessary and
are correctly retained. An intermediate-price broker interval **does not close
Q3**, because the identical ordinary kernel has the same output and bill.

The independent checker reconstructs every line from sealed public records and
existing private development truth, rather than accepting the analyzer's line
list as its starting point. It verifies **234 records and 21,248 trace positions**,
then all **103 price-optimal record intervals** across nine scenario/seed groups.
A second construction, based on every nonnegative rational crossing and each
intervening cell, independently verifies completeness and endpoints. There are
**39 positive-width intervals, 64 zero-price-only ties, and no singleton optimum
at a strictly positive price**. These counts include distinct records with
coincident objective lines; they are not numbers of independent experiments.

## Exact mathematical reconstruction

For a fixed transcript j, let E_j be its terminal error count and L_j its actual
local-unit bill. Every line receives the common installed-source charge 50,115:

```math
C_j=L_j+50115,\qquad f_j(\lambda)=E_j+\lambda C_j,\quad \lambda\geq0.
```

The error unit price is one. Optional report production is excluded, consistently
with the terminal-answer-service comparison. The exact set where j attains the
catalogue minimum is

```math
I_j=[0,\infty)\cap\bigcap_i\{\lambda:(C_j-C_i)\lambda\leq E_i-E_j\}.
```

Write a=C_j-C_i and b=E_i-E_j. If a is positive, the inequality supplies the upper
bound b/a. If a is negative, it supplies the lower bound b/a. If a is zero and
b is negative, no price is feasible; otherwise that comparison adds no bound.
The intersection is empty, a closed finite interval, a closed singleton, or an
unbounded tail. Starting the lower endpoint at zero excludes negative-only
solutions. The analyzer uses the equivalent de=E_j-E_i and dc=C_i-C_j convention;
its sign handling is correct.

For each reconstructed nonempty interval, the checker verifies the archived
endpoints, positive-width flag, objective coefficients, rational witness,
witness objective, coincident-line list, and ordinary-equivalence flags. Every
witness is checked against every eligible line. A coincident line means exactly
the same E and C. Other lines that tie only at a crossing are represented by their
own closed intervals and are recorded separately as endpoint ties in
`details.json`.

Witness checks alone would not establish that every optimal line was retained.
The second construction therefore forms every pairwise crossing at nonnegative
price, includes zero, evaluates all crossing points and rational midpoints between
them, and evaluates an unbounded-tail witness. Affine order cannot change inside
one of these cells. Joining each line's active cells reconstructs its complete
optimal interval. This uses 2,210 distinct crossing points counted across groups
and 4,420 point/cell evaluations; it reproduces all pairwise-intersection results.
It also verifies that using local bills in place of C_j leaves every endpoint
unchanged, since the common source term cancels in pairwise differences.

These are price-optimal sets, not a claim that every zero-price-only record is
strictly Pareto efficient. At price zero, all zero-error records tie even when
one has a larger resource bill. The declared closed-interval contract correctly
retains those records instead of silently discarding the zero-price boundary.

## Eligibility and the source-accounting transfer

The 234 unique sealed records comprise **123 ordinary controls and 111 broker
records with identical ordinary-kernel interpretations**. Each group contains
all 19 available ordinary lines: eight deterministic controls, one probability
controller, and both ordinary-combination indexes at all five frozen acquisition
parameters. No ordinary method, supplied constant, expensive exact method, or
unfavorable acquisition transcript is filtered out.

The eight deterministic methods are proof_enumeration, proof_dpll,
exact_enumeration, exact_dpll, exact_cache, exact_cache_hashed, no_compute_0, and
no_compute_1. Their source creates no random bit tape; the recorded executions
have zero bits consumed and no randomness record. They were intentionally run
once at seed11 and may therefore be reused for seeds29 and47 of the same scenario.
Learning and broker records retain their own seed. The repeated participation of
these existing deterministic records gives **282 eligible group-line appearances**;
it does not create 282 executed policies or new independent observations.

| Scenario | Seed | Eligible lines | Positive-width frontier records | Zero-price-only records |
| --- | ---: | ---: | ---: | ---: |
| cold_mixed | 11 | 32 | 4 | 7 |
| cold_mixed | 29 | 26 | 5 | 5 |
| cold_mixed | 47 | 26 | 3 | 7 |
| repeat_online | 11 | 38 | 6 | 5 |
| repeat_online | 29 | 38 | 4 | 5 |
| repeat_online | 47 | 38 | 8 | 5 |
| cheap_structure | 11 | 32 | 3 | 10 |
| cheap_structure | 29 | 26 | 3 | 10 |
| cheap_structure | 47 | 26 | 3 | 10 |

The older common_v2 records paid 48,274 installed-source units. The corrected
reuse archive paid 50,115. Comparing the actual paid source manifests, every
existing source is unchanged and the only added paid core file is
`v3/experiments/p308_cached_service.py`, 6,924 bytes. Its tariff is

```math
2\left\lceil6924/8\right\rceil+\left\lfloor(6924+72)/64\right\rfloor
=2(866)+109=1841.
```

Thus assigning L_j+50,115 to an old line adds exactly 1,841 source units and
changes neither its acquisition parameter, local operations, terminal outputs,
nor observed errors. All 48 new lines already paid the same bill. The analysis
is an explicit accounting transfer, not a policy rerun.

There is one limited implementation guard worth distinguishing from the verified
artifact claim. The analyzer's `source_before` superset assertion proves only
that old source hashes still occur unchanged; by itself it does not prove the
exact added paid-source set or derive 1,841. Those stronger facts are verified
here from each actual source invoice and paid manifest. The larger experiment
source capture also includes the new analysis runner, which is outside the paid
common core. This guard limitation causes no discrepancy for this bound archive;
a generalized future utility should derive the transfer from exact paid
membership instead of treating the hash-superset check as that proof.

## Compact exact seed11 frontier

The table shows positive-width intervals. Intervals are closed at finite
endpoints, so neighboring rows tie there. At zero price there are additional
zero-error-only ties preserved in the complete result. C includes the common
50,115-unit source charge. A dagger marks a broker line with its identical
ordinary-kernel interpretation.

| Scenario | External λ interval | Optimal recorded line(s) | E | C |
| --- | --- | --- | ---: | ---: |
| cold_mixed | [0, 3/170585] | ordinary_combo_hashed, frozen acquisition 1/100000 | 0 | 1,068,642 |
| cold_mixed | [3/170585, 10/429931] | ordinary_combo_hashed, frozen acquisition 1/10000 | 6 | 727,472 |
| cold_mixed | [10/429931, 15/232888] | finite_tickets† | 16 | 297,541 |
| cold_mixed | [15/232888, ∞) | no_compute_1 | 31 | 64,653 |
| repeat_online | [0, 16/616323] | exact_cache_hashed | 0 | 1,924,600 |
| repeat_online | [16/616323, 4/118297] | value_tickets_hashed†; reuse comparison: tickets, hard1, cold provider† | 32 | 691,954 |
| repeat_online | [4/118297, 5/64501] | proof_enumeration | 44 | 337,063 |
| repeat_online | [5/64501, ∞) | no_compute_0; no_compute_1 | 64 | 79,059 |
| cheap_structure | [0, 32/15339] | exact_cache | 0 | 74,630 |
| cheap_structure | [32/15339, ∞) | no_compute_0; no_compute_1 | 32 | 59,291 |

Equivalently, the seed11 switch prices are:

- **Cold mixed:** 3/170585, then 10/429931, then 15/232888.
- **Repeated tape:** 16/616323, then 4/118297, then 5/64501.
- **Cheap structure:** 32/15339.

At the displayed hindsight price λ=1/30000, the seed11 winners are finite_tickets
on cold mixed; value_tickets_hashed and its coincident reuse-comparison cold
record on the repeated tape; and exact_cache on cheap structure. The old and
reuse cold records at the same repeated-tape line are duplicate evidence about
one price geometry, not two independent successes.

For example, the cold-mixed finite_tickets line is (E,C)=(16,297541).
It first ties the frozen acquisition-1/10000 hashed ordinary combination
(6,727472) at 10/(727472−297541)=10/429931, and ties the no-compute-1 line
(31,64653) at 15/(297541−64653)=15/232888. Every other eligible line is also
above or tied on that entire closed interval, as the full intersection verifies.
The analogous repeated-tape broker interval comes from (32,691954), between
(0,1924600) and (44,337063): 32/1232646=16/616323 through 12/354891=4/118297.

## Acquisition price, retrospective selection, and Q3

Each ordinary-combination transcript was generated using its recorded acquisition
parameter. The external λ in this analysis changes only the retrospective
coefficient on its already recorded cost. For example, repricing the
acquisition-1/100000 transcript above does not regenerate its choices as if its
native acquisition parameter had become the displayed λ. Accordingly this
frontier answers a different question from the earlier native-price comparison,
which restricted each combination method to its matching acquisition price.
Both scopes can be correct; neither result should be substituted for the other.

The envelope also uses hindsight over the recorded errors and costs. It is not
an implemented selector for an unseen tape, a learned acquisition policy, a
new intermediate-price native run, or a guarantee for such a run. The evidence
is retrospective DEVELOPMENT on already exposed inputs.

Finally, `p308_mirrors.run_ordinary_mixture` returns the same generic
`p308_broker.execute` call with the supplied service, tape, contract, and keyword
arguments. This applies to the cached-service variants as well as the original
cold broker under their existing ownership premises. The wrapper's elementary
ordinary expected-cost interpretation requires no different output service.
Every broker frontier line therefore has an ordinary implementation with the
identical E and C at every price. The 111 flags express this inherited executable
equality; they do not fabricate 111 separately measured mirror runs. The observed
intermediate-price role among other recorded controls cannot establish strict
superiority over a comparison class that contains that same kernel, and it
**does not resolve the outstanding Q3 contribution issue**.

## Reproduction, source binding, and actual issues

The full source/input manifest is `plan.json`; all 234 reconstructed line records
and all 103 verified frontier records, including endpoint competitors, are in
`details.json`. The checker never imports or calls the analyzer or policy code.
Its first execution ran **17:42:55.113457–17:42:56.307048 UTC** and passed. These
observed executable times are not research credit.

Manifest setup initially looked for the common archive's plan under the wrong
filename and stopped before writing a plan or running the checker. The plan
records that correction to the actual `run_contract.json` path. No substantive
assertion failed, and there was no policy or analysis retry.

The separate structural reviewer independently checked the source-bound algebra,
closed singleton handling, and coincident-line semantics statically, without
executing this checker or adding principal credit. Its conclusion agrees. This
review's stronger paid-manifest reconstruction also answers its source-transfer
provenance question.

| Artifact | SHA-256 |
| --- | --- |
| Analyzer | `6bc2cca5600477e86957382f8af7fc99599c5ab09f374629dbc7ed2cb64fc7b8` |
| Analysis contract | `2391f9380aef8eadcb0103c0c1701acea5a2709ef9fa5adc28b79a6d1de2edf4` |
| Root result | `2bc29b62e9713ba90665605edab95c60e025250c7c8a210276d33fb6f9b147d7` |
| Ordinary mirror | `06d39c3c865398eed8baa51920d1c3ad5cfbd2d37190e308e869fc15a0ea5aec` |
| Review plan | `42fb08c5fe515f4fc93e7eea1e52084a687a0719f92a0c0ff9faa7cdf22e8b0a` |
| Independent checker | `daa3271429a5a321db7886d2d71c707e2bb1765434574bbf1cf768287fe88242` |
| Independent result | `a331a56367d6196f79d3dbabfc24175c58d1e90def1f4a38c391c8cf75de7351` |
| All reconstructed lines and intervals | `a12e79e1648aaadf0726e4f6730b58891abe9558fb438a4d275dc039311d9803` |

The sealed score sources are common_v2
`4b34e6cf9befd537235950d7bf12c3ea750a568cf6863a0da190787d217e103f`
and reuse_v1.1
`95e3f731d3d1e2645db9714812dcca94808314796759a2d947ec45ea315d0364`.
Both public/private seals and every public record hash were verified. Error
reconstruction uses those existing evaluator targets; it does not independently
re-prove the CNF oracle or claim a new population-level statistical result.
