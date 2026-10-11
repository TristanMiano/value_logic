# Independent preparation and execution-boundary review

Contributor: **ChatGPT (GPT-6 Astra Pro)**. Same-model, nonblind independent
review, October 11, 2026 UTC. Principal research credit: **zero**.

**Verdict:** no remaining material blocker was found in the reviewed preparation
and lifecycle boundary, under the stated ownership of stable source and runtime
files. The amended implementation resolves the concrete startup, copied-byte,
and task-selection defects identified during this review. This verdict does not
assert that preparation has run successfully: the principal owns that separate
execution and its resulting receipt.

## 1. Exact sources and permitted work

The [source manifest](source_manifest.json) preserves all **50** declared freeze
sources, plus five review-context files. The lists were reconstructed from
literal source declarations using `ast`, without importing an experiment or
calling an adapter. Their relative paths are retained under `source/`. The
manifest's SHA-256 is
`2b0054b62ce7691076afbca21722a791c4e76ca4848e9ae8df42e9b520555d3f`.

| Reviewed source | SHA-256 |
| --- | --- |
| [Final preparation driver](source/v3/experiments/p309_freeze.py) | `15c49d3ba6a39231d954a0cd36818d9b64f4e64a58e047d26d3f446744f5a709` |
| [Lifecycle](source/v3/experiments/p309_lifecycle.py) | `5b8ff096f03cd6ecafaf8acb6db59ecc0a8cbb9f9ab963fa7844b3c0adf246bb` |
| [Prospective configuration](source/v3/experiments/protocol.v1.json) | `dde9fe405ad39e65db3d49cb47d298e3ab6e498d7c5c485ff215ff884466b88f` |

The [selection](source/v3/work_logs/P3_09_2026-10-11_S1/selection.json)
authorizes P3-09 and explicitly withholds final evaluation. Consistent with the
[review plan](plan.md), this review performed canonical reads, preserved source
copies, and ran only the small bytecode toy described below. It did not invoke
`prepare`, `verify`, `development-checks`, any final stage, an experiment
generator, a policy, or a private scorer. No canonical source, ledger, clock,
prior evidence, or task-state file was edited.

## 2. Runtime and executed-source identity

The final driver requires the documented Linux, little-endian CPython 3.12.14
environment. Its startup guard requires the behavior flags corresponding to
`-E -S -B`, optimization zero, exactly the declared cache-prefix `-X` option,
and no command-line warning options. It verifies that `/dev/null` is character
device `1:3`. The exact prefix is:

```text
/dev/null/value_logic_p309
```

This is a concrete source-loading rule. In the supplied CPython implementation,
[`cache_from_source`](runtime_primary/importlib/_bootstrap_external.py) derives
the candidate cache path beneath `sys.pycache_prefix`. `SourceLoader.get_code`
attempts that bytecode read and, on an `OSError`, reads and compiles source.
The `dont_write_bytecode` condition controls subsequent cache writing; it does
not suppress the earlier cache read. A descendant of the verified non-directory
null device cannot supply that derived cache. Direct source-less `.pyc` modules
are separately rejected by the origin guard. Built-in and frozen implementation
code remains part of the bound interpreter.

The [executed development probe](bytecode_probe.py) constructed only a module
whose cached code returned `17`. It then replaced the module's source with
equal-length source returning `99`, retaining the timestamp used in the cache
header. It used the standard-library
[`py_compile`](runtime_primary/py_compile.py) API with explicit timestamp
invalidation, and two fresh interpreter processes.

| Import command prefix | Observed value | Reported source path |
| --- | --- | --- |
| `python3 -E -S -B` | `17` | The current toy `.py` file |
| `python3 -E -S -B -X pycache_prefix=/dev/null/value_logic_p309` | `99` | The same current toy `.py` file |

The [results](bytecode_probe_run/results.json) are PASS; source and cache bytes
were identical before and after both imports. This demonstrates the specific
gap in relying on `-B` or `module.__file__` alone, and the effect of the adopted
prefix on this timestamp-valid cache. It is not an experiment-method run.
The exact used cache is preserved as the normally tracked
[used_cache.pyc.bin](bytecode_probe_run/used_cache.pyc.bin), **289 bytes**, SHA-256
`fb1d379c2f18fce566997721da54b9a89ce426537760abd6b6b3b40269ca9ae9`.
The [archive receipt](bytecode_probe_run/bytecode_archive.json) binds that copy
to the already executed probe and confirms its script remained unchanged.

`runtime_record()` inventories supplied standard-library source/extension bytes,
the interpreter, and its enumerated native dependency closure. It records
behavior flags, warning options, `-X` options, integer-string limits, and text
encodings. The copied-source development process returns the digest of its own
runtime record; preparation requires equality with the parent's captured record.
Consequently the preparation receipt cannot silently use a parent's permitted
settings while exercising a differently configured child. The supplied unused
Tk dependency exception is named explicitly; it is not a blanket exception for
missing native libraries.

The local origin guard includes `__main__` when it has a file, checks imported
repository modules against declared paths, and rejects source-less bytecode,
site/distribution packages, and files outside the repository or supplied
standard-library closure. Adapter and lifecycle paths have additional exact
checks; the analyzer path is checked during development preparation. The
50-source freeze closure is distinct from each arm's paid installation bundle;
this review does not add all frozen contract documents to a method invoice.

## 3. Copy, preparation, and publication ordering

The relevant sequence in the reviewed driver is:

1. Capture the prospective source rows and runtime, with a durable preparation
   attempt record.
2. Read each source payload; require its byte length and hash to equal its
   captured row before publishing the copy.
3. Verify the entire copied closure before invoking the copied entry point in
   a fresh interpreter with the exact startup flags.
4. Require explicit PASS and no-final-generation metadata, matching child
   runtime digest, unchanged live source/runtime, and unchanged copied bytes.
5. Prepare the manifest and receipt, check live and copied sources again before
   the directory rename, then verify the published freeze.

This resolves the earlier copy-window issue: a source temporarily changing
from `A` to `B` and back could previously leave `B` in a copy while both live
manifest observations saw `A`. Now the payload copied in that window must itself
match the captured bytes before the child may run. The copy is rechecked before
publication. A failed attempt retains its available stdout, stderr, failure
record, and any supplied paid failure record; successful publication reuses the
checked directory instead of regenerating its content.

The check remains a protocol over owned files. It is not a continuously atomic
filesystem snapshot or a defense against an adversarial writer changing the
copied sources during execution. Every final stage verifies the bound source
and runtime on entry. It does not continuously attest all process memory or
the kernel between individual opcodes. Stable, unmodified source/runtime
ownership through a stage is therefore a real assumption, which must accompany
the claim of source-bound execution.

## 4. Preparation is separate from final exposure

`block_final_generation()` wraps each loaded adapter's public `generate`
attribute for the whole preparation selfcheck interval. It rejects the accepted
final token before calling the underlying generator. The supplied selfchecks
may exercise explicit development toys, but the preparation driver does not
materialize the final recipes. This guard prevents accidental use of the
selected public endpoint; it does not claim to sandbox deliberately hostile
code that bypasses that endpoint.

`require_p310()` rejects any task other than `P3-10` before freeze or exposure
lookup. For `P3-10`, it also requires the repository pointer and a **unique**
P3-10 chunk marked `in_progress`. A pointer advertising P3-10 as the next task
while its chunk remains `unstarted` is insufficient. This closes the
distinction between recommending the next task and actually selecting it.
The repository's authorized owner remains responsible for changing that task
state; the check is not an independent authentication of a user's identity.

The final path verifies the freeze before creating the irreversible exposure
marker, and publishes/fsyncs that marker under the writer lock before the first
generator callback. A failed first generation still counts as exposure.
Complete sealed inputs precede public work; all public units must be sealed
before private scoring; all score units must be sealed before analysis.
The stage and output root are fixed by the frozen implementation and schedule.

## 5. Completion, failure, retry, and unknown cost

The reviewed `Stage` implementation publishes a unit start before invoking its
callback. It publishes result bytes and a separate hash-bound seal afterwards.
Only the seal grants completion. Missing or altered result/start bytes are
rejected, and a summary cannot replace them. A missing derived stage-completion
index may be reconstructed from all valid unit seals without another callback.

An internal method's returned failure is a completed observed outcome, including
its available invoice. It cannot be retried as an infrastructure failure. An
unreturned callback or outer orchestration failure retains its attempt history;
an unchanged retry requires the recorded infrastructure classification and
reason, preserves every completed unit, and is limited to the second attempt.
Deterministic defects require a separately preserved amendment. The lifecycle
records that distinction; it does not automatically establish that a supplied
investigator classification is scientifically justified.

`execution_history()` retains unsealed public attempts as **unknown cost** even
if a later attempt supplies a completed path. The
[captured analyzer](source/v3/experiments/p309_analyze.py) gates its overall
positive economic-saving predicates on complete outer public-attempt accounting.
Its completed-path arithmetic can remain descriptive. Neither missing invoices
nor unsealed partial results become zero-cost work. Process time/RSS observations
are separate from the deployed abstract tariffs; the RSS field explicitly is a
process high-water mark rather than an additive per-unit allocation.

No additional worker tests are needed for this bounded review. The preserved
bytecode demonstration, final source readback, and source-convention receipt
support this audit's narrower conclusion; successful principal preparation and
future authorized final execution remain distinct records.
