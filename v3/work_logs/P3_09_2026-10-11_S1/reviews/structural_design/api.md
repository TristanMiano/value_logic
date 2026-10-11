# P3-09 certificate adapter API

Contributor: ChatGPT (GPT-6 Astra Pro), October 11, 2026 UTC.
P3-09 preparation; zero principal-clock credit.

Canonical file:
[p309_certificates.py](../../../../experiments/p309_certificates.py).
The source-bound design, tariff and scope are in [design.md](design.md).
The current adapter version is `p309-certificates-v1.1`; its
[exact-type scorer amendment](scorer_v1_1_amendment.md) preserves the earlier
v1 paid development closure and strengthens only independent terminal audit.

| Callable | Input/output and authority |
| --- | --- |
| `source_paths()` | Eleven repository-relative application paths; no workers or cases instantiated |
| `default_config()` | Fixed recipes, rosters, accounts, caps and full independently prepared source record; source bytes are read, no cases made |
| `validate_config(config)` | Exact fixed metadata and canonical complete source-record shape; live byte authentication remains paid enrollment |
| `groups(config)` | Four metadata-only dictionaries with `id`, `arm='certificates'`, `recipe.family`, `recipe.nbits`, `request_count=4` |
| `units(group, config)` | Twenty-six whole-history units per group; seven fresh/six resident methods under each of two accounts |
| `generate(group, config, *, exposure_token)` | Exact token `P3-10-EXPOSED` required before formulas; returns canonical public current/old Frame records, witnesses and bounds |
| `run(unit, public_input, config)` | Full four-attempt paid history, all invoices/raw counters/output/failure states and losslessly captured audit packets; no independent scalar oracle |
| `score(unit, result, public_input, config)` | Separate independent exact truth/output/invoice audit; semantic invalidity returns `status='FAIL'`, all paid costs and no invalid covered identity |
| `selfcheck()` | Explicit disjoint two-bit DEVELOPMENT toys only; returns top-level `status='PASS'`, raises on a failed check, never calls final groups or generator |

## Unit metadata

Every unit has these top-level fields:

```text
id, group_id, arm, method, method_kind, recipient,
budget_condition, configuration_id, budget, consumer_budget, request_count
```

`method_kind` is `candidate` only for `P-REUSE`. `P-FRESH` and all `O-*`
methods are ordinary. `budget_condition` is `full` or `capped`. Configuration
IDs combine method, recipient and budget condition; unit IDs additionally
include the stream ID. Each unit owns one fresh process-level Session object;
every scheduled request inside that unit sees its actual predecessor state.

The group recipe family is `majority_dnf_cnf` or `selector_mux_sum`; its only
size strata are four and seven bits. Group/unit enumeration does not construct
the expressions described by those recipes.

## Public inputs and paid results

The public record has the schema/version/stage, group ID, recipe metadata,
coordinate count/order, an old-input list and four current cases. Each old
input contains a full canonical `frame_record`, integer-bit `witness` list and
exact rational `bound` string. A current case additionally has its slot and
stable shared identity `group_id + '.r' + slot`, with slots one through four.
No private truth-table output is included.

`run` creates a new owner and calls the unchanged paid delivery governor four
times in order. The subclass converts current and old records inside paid
worker stages. Each paid row retains the inherited receipt identity
`group_id + ':' + slot`, status, terminal output, raw work, exact invoice,
source/input/proof/retained-byte diagnostics and error disposition. The row
also carries its stable shared request identity and observer corroboration
of current receipt presence and previous receipt withdrawal.

Audit byte packets become JSON objects with `stage`, `category`, `bytes`,
`sha256` and `payload_base64`. Encoding these already paid bytes for the
experiment archive is observer work, not new receiving authority. The original
service charge remains in the invoice.

## Standard score fields

The parent's aggregate analysis consumes:

```text
status, validity_pass, request_count,
all_request_ids, delivered_request_ids, total_units,
category_totals, method, method_kind, recipient,
budget_condition, configuration_id, group_id, unit
```

Stable request identities align across every method in one stream. The
independent scalar reference assesses the complete current incumbent sublevel
and includes hard-domain/minimizer/sublevel counts and exact extrema in the
separately scheduled score output. A false or wrongly scoped delivered
certificate is a completed invalid score, not a callback exception eligible
for an unexplained-infrastructure retry. Its invoice remains included. Outer
input, unit or result-binding mismatch raises before semantic comparison.

`total_units` includes every paid attempt, source enrollment, old construction,
storage period, failed prefix and terminal receipt. It is `null` if an invoice
does not reconcile. Known category prefixes are still returned and marked by
`category_totals_complete=False` in that case. No partial unknown bill is
substituted for a complete price.

`category_totals.producer` means all nonconsumer units;
`category_totals.consumer` follows the inherited stage classification. These
two add to the total. The `output`, `storage` and `source` fields are overlapping
diagnostics and must not be added to those two fields as a second total.
`tariff_category_totals` separately retains the primitive category partition.
The inherited retrospective `consumer_thresholds` flags are preserved in raw
paid rows but never used as actual funding claims or to generate capped paths.

## Reproduction and path restoration

The initial development closure is stored under
[development_smoke_v1/source](development_smoke_v1/source/) with repository
relative directories preserved. To replay the explicit development toy check,
use a fresh interpreter from that `source` directory:

```bash
PYTHONDONTWRITEBYTECODE=1 python -c 'import sys,json; sys.path.insert(0,"v3/experiments"); import p309_certificates as C; print(json.dumps(C.selfcheck(),sort_keys=True))'
```

Do not flatten the source paths. The application enrollment reads files under
its restored repository root and verifies exact expected lengths and hashes;
the canonical module loader also checks its source root. CPython 3.12.14 is
required by the inherited tariff. The source snapshot alone is an application
closure; the parent freeze separately binds interpreter, standard-library and
native-runtime dependencies.

This command is a DEVELOPMENT check. It creates no final cases, no final
population or random seeds, and no principal research-clock credit. The
parent preparation gate may rerun it on its frozen application/runtime copy;
final generation remains separately blocked until P3-10 authorization.
