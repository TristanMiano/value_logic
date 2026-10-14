# s08 publication validation

Contributor: **Codex (GPT-6)**. All work here is administration with zero
research credit. Scientific run-specific checks are documented in the branch
findings and retain their own failures and retries.

The Windows Python 3.13 and bundled Python 3.12 monolithic suites terminate
with access violations in unchanged historical tests (`verification_1.txt`
through `verification_3.txt`). A process-isolated pass over all 82 test modules
completes 1,536 tests in passing modules, retaining unsuccessful modules and
all five allowed attempts in `isolated/`. This is **not a full-suite pass**.

Ubuntu WSL Python 3.12.3 also terminates with segmentation faults in unchanged
historical arithmetic/semantics. Single-CPU-affinity attempts at CPU0 and CPU7
retain their logs. The fault's cause is unproved; the user's reported CPU
instability is context, not a diagnosis. Successful retries do not erase failures.

The checks separately reveal Windows fixture assumptions (native path spelling
and newline translation in temporary portable-view fixtures), and Linux use
of an existing Windows CMake cache. These are not new scientific source changes.
No historical implementation or frozen fixture was rewritten to force a pass.

Publication restores newline-only working-copy conversions to exact committed
bytes, recorded in `restored_checkout_bytes.json`, `restored_cpp.json` and
`ledger_prefix.json`. The old ledger prefix is exactly the Git blob; s08 appends
139 raw segment rows and six nonadditive correction notices. Local Git newline
conversion is disabled. Historical source objects and relocations remain intact.

The complete Markdown guard passes: 1,448 documents, 18,861 math spans,
64 verified portable views, zero active issues, 376 preserved-source issue
records. The new aa01 declaration retains its executed design hash; the
mechanically derived view is registered in `tools/math_views.json`.
Evidence relocation verification passes: 32 paths, 30 unique objects,
5,350,075 original bytes. Logs: `math_3.txt`, `evidence_2.txt`.

The recurrence source preserves all 18 preceding JSON row objects and Markdown
rows. There is exactly one table, now 19 rows with s08 last. Old source dates,
scope IDs and carried ages remain distinct from new bc02/gc02 observations.
The final research total remains 14,402,318,580,700 ns; no test adds credit.

Staged path checks and remote CI results are recorded below after execution.

Staged path checks pass:22,965 files,3,962 ancestor attribute probes, longest relative path200/200 UTF-16 units and full Windows path236/259. The24 portability/evidence/link-relocation unit tests pass. Later small publication files are rechecked before commit. `git diff --check` reports preserved blank lines in executed Python sources and whitespace in raw failure logs; these raw records are retained unchanged. Standalone local link attempt1 also crashes; remote CI remains pending at this commit.

## Post-crash completion

The saved research commit is `d75b3ff49acbb31404844731c54c1bb917c8e66c`. Research remains closed. Three executed declaration copies now have verified original link namespaces; the aa01 portable view was mechanically rederived with that namespace. Raw declarations and the scientific manifest remain unchanged. The complete local link checker passes on1,449 documents (`links_2.txt`). The first branch upload ended with HTTP408; remote readback found no branch, so a transport retry is required.
