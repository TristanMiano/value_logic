# Independent ordinary-control review of the common runner

Stage: **DEVELOPMENT**. Reviewer: ChatGPT (GPT-6 Astra Pro), same-model,
nonblind delegated review. Source/plan inspection only, while the parent-owned
public execution was running. No private scoring call, run-result inspection,
or gzip read. No added principal-clock credit or edits to the executing source.

## Reviewed identities

| Source | SHA256 |
| --- | --- |
| `development/comparison_plan_v1.md` | `82f26bb0a5db10e37304b5854f29dcdc61b1ef903882d75bb9160a7948274a1d` |
| `development/common_v1/source/v3/experiments/p308_run.py` | `09010018bc7b126b896ad10edc5b35faa4aa39382311c868332a394a038faf81` |
| copied `p308_broker.py` | `399080c950a48c1cd935efbee8ed7769a7af54b7afa14859b5671397638e2e4d` |
| copied `p308_ordinary.py` | `492897ba8eb84921068411c411188bd0057d299668904c31c3bf877d9db9e9af` |
| copied `p308_mirrors.py` | `06d39c3c865398eed8baa51920d1c3ad5cfbd2d37190e308e869fc15a0ea5aec` |

## Material findings

1. **Incomplete records are scored as prefixes, and prefix equality can pass
   the paired check.** `private_score` uses `zip(episode["trace"], tape_truth)`
   and records, without requiring, `full_horizon`. A pending issued ordinary
   output is absent from `trace` but is retained in `issued_trace`; the scorer
   does not inspect that field. The broker retains only its pending request ID
   in its current audit record. The paired loop similarly uses `zip` without
   requiring both lengths equal the declared horizon. Therefore incomplete
   executions could receive artificially small error totals and a paired
   equality label supported only by their common prefix. This has no realized
   effect if the parent independently confirms every main episode completed
   successfully at the full horizon. Otherwise retain failures as incomplete
   service, score all actually issued outputs where available, and exclude
   incomplete totals from a full-service economic ranking. Require full
   declared length and chronological identity for the paired success claim.

2. **The economic method list omits a no-purchase fixed action.** Both bounded
   proof arms spend up to 2048 units per query. Every learning/combination arm
   purchases at least the selected query per block, apart from its paid cache
   hits. Constants inside the expert library still incur that learner's
   feedback purchases. The high-resource-price frontier therefore omits a
   basic executable ordinary option. A prospective pair of `proof_only`
   executions with `proof_cap=0`, separately supplied fallback actions 0 and 1,
   already fits the immutable-output and common-source service. It conservatively
   retains the controller/provider rejection overhead even though no provider
   computation is funded. Either add both without truth-selecting one, or
   explicitly restrict the reported frontier to the supplied method list and
   disclose this missing endpoint. A direct constant policy could be cheaper
   still under a separately declared output service.

These findings were sent to the parent before this review inspected any new
private scores. The requested economic analysis remains pending the parent's
public seal and principal-owned scoring.
