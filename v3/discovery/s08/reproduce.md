# Reproducing s08 evidence without reacquiring it

Contributor: **Codex (GPT-6)**. Publication administration; zero research credit.

Start at the actual repository root. [Checkpoint](cp01.md) and
[findings](findings.md) identify the current result and its limits. Each run
directory keeps its executed design, implementation/dependencies where frozen,
source records, receipts, result and checker output. Failed prefixes and logs
are scientific history. Do not overwrite them with a successful rerun.

`effective_actuals.json` is authoritative for credit. `actuals.json` is raw.
Running `python -B v3/discovery/s08/reconcile.py` reconstructs closed segments,
exclusions and exact totals; it never restarts the clock. It also appends
idempotent correction notices if missing. Do not run `clock_source.py` or
`clock_resume.py` to inspect this closed session.

## Read-only scientific reconstruction

Use saved result files and the corresponding `check_*.py` entry point.
For example, `check_bc02.py c0 budget` reconstructs that unit, and
`check_gc02.py n8_path lazy` reconstructs a general-graph unit. Inspect each
script's argument parser first: names and arms are taken from its saved
`design.json`, not inferred from a directory spelling. These checks may write
new diagnostic results and logs but must not call acquisition. Use a new short
output location for diagnostic comparisons when exact earlier checker bytes
need preservation. The aggregate reconstruction drivers can skip completed
units; an unchanged summary alone is not evidence of a new full check.

Checkers are authored in this session and are independent recomputations of
the selected quantities, not external scientific review. Small-world checks
are exhaustive only within their recorded finite domains. Large graph checks
depend on the admitted geometry theorem, and some capped diagram work remains
unresolved. Read the scope in the branch findings before interpreting a pass.

The live source files sometimes evolve after a frozen run. To execute an old
version, restore its exact dependency set in a separate short checkout with
the original relative import layout. Do not directly execute a nested frozen
`impl.py` if it locates siblings through `__file__`: doing so can silently
select the wrong dependency or fail to locate s05/s06 services. Compare hashes
against the executed design. Use Git blobs or short immutable paths, preserving
the repository's 200 UTF-16 relative-path limit.

## New acquisition is a different operation

`run_*.py`, service acquisition entry points, and prepare functions may perform
new physical queries, proof calls or expensive compilation. They are not a
free verifier of old evidence. For a new development run, declare fresh seeds,
menus and fees, use a fresh output directory, record all failed work, and
start a new observed research session only when authorized. New outcomes on
an exposed family are development, not fresh confirmation.

Python 3.13.14 and bundled Python 3.12.14 both suffered intermittent failures
on this host, including access violations and inconsistent runtime-object
errors. Cause is unproved. Cold retries and a second runtime often completed
unchanged finite checks. Logs preserve attempts; incomplete costs stay unknown.
The later compact JavaScript finite checks use Node and exact integer counts
within their stated ranges. They do not substitute for actual proof calls.

## Publication integrity

The s08 subtree disables newline conversion so hashes survive Windows checkout.
Publication also restored unchanged CRLF-only historical working copies from
their exact Git blobs; the restoration manifest records every path and hash.
No historical scientific blob was edited. The local repository now disables
automatic CRLF conversion. This maintenance earns no research credit.

Use the current [math guide](../../../docs/math_markdown.md),
[checkout guide](../../../docs/windows_checkout.md), and
[archive-link guide](../../../docs/archive_links.md). Required commands include:

```powershell
python -m verification
python v3/checks/math_markdown.py
python tools/check_repo_paths.py
python tools/check_repo_paths.py --checkout-root C:\Users\trist\projects\value_logic
python tools/evidence_paths.py verify
```

Path validation checks the staged index, so stage intended changes first.
Publication logs and the final validation record live in `pub/`. Failed suite
attempts are retained, and any process-isolated fallback is reported as such.
These repository gates are separate from scientific confirmation.
