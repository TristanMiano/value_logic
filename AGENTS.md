# Working in this repository

**Start with the [project charter](v4/CHARTER.md).** It states the project's
theses and sits above every phase plan, protocol and audit. Read its
**Drift** section before starting any task, and follow the binding
[aim-balance policy](v4/AIM_BALANCE.md): hunt for the kernel of truth
in a thesis, the most faithful reading that can be proved (optimizing
faithfulness and defensibility together, never retreating to its negation or
to the easiest statement), prefer informative positive conditional statements to
bare negations, pair every search for failures with an equally explicit
search for constructions, and perform its end-of-task review after every task,
including documentation edits. The author approved the charter on November 8,
2026. Phase-four work follows [TODO_v4.md](TODO_v4.md) and the
[four-hour recurrence procedure](v4/RECURRENCE.md). Inspect the active cycle and
its observed timing before starting or resuming research; a context refresh
does not start a new cycle. The phase-three notes below are historical.

Use the actual checkout root. Preserve unrelated local work and historical
scientific records. Attribute new research to the model actually doing it.

For phase-three research, read the current state in [TODO_v3.md](TODO_v3.md)
and [v3/RESEARCH_PROTOCOL.md](v3/RESEARCH_PROTOCOL.md). The next discovery task
is described in [the current continuation prompt](v3/discovery/CONTINUE.md); inspect
current session records before starting or resuming its clock.

## Portable evidence and paths

- Keep every tracked path, including ancestor `.gitattributes` lookups, within
  **200 UTF-16 code units relative to the repository root**.
- Use short output directories. Avoid nesting a full repository path inside
  an already deep review snapshot. Prefer Git commit/blob references or short
  immutable object paths with a manifest when exact historical copies are needed.
- Historical snapshot locations listed in
  [the relocation manifest](v3/evidence/relocations.v1.json) resolve through
  `python tools/evidence_paths.py resolve ORIGINAL_PATH`. Preserve object bytes
  and historical manifests; see [the checkout guide](docs/windows_checkout.md).
- Before committing, stage intended changes and run
  `python tools/check_repo_paths.py` (it checks the index). For evidence changes,
  also run `python tools/evidence_paths.py verify`.

The research protocol controls attribution, research clocks, continuation and
confirmation. Repository maintenance and handoff preparation earn no research credit.
