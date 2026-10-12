# Working in this repository

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
