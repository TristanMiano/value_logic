# Receipt-path schema check

Date: 2026-10-09. Scope: operational validation only; zero Research90 credit.

The existing `receipt_path` pattern accepts
`v3/work_logs/P3_06_2026-10-09_S1/publication/applied_package.json`.
It also accepts a nested receipt under the same directory, as the helper permits.
Both Python's `re` and ECMAScript's `RegExp` in the tool's V8 runtime passed all
eight positive and negative cases recorded in [results.json](results.json).

The apparent extra escaping is valid: the decoded character class excludes a
literal backslash, and the extension uses an escaped literal dot. Missing-dot,
wrong-extension, uppercase-extension, backslash, wrong-directory and absolute
path variants were rejected. No functional pattern bug was found, so the schema
was not edited or replaced. Its exact SHA-256 remains
`ee71a7336d5ae478868b5e42ad82580ff6d7b505b3e6c670e162ad989bf1ccf4`.

This is a narrow regex-property check, not full validation by a JSON-Schema
library. The helper retains its additional path and cross-field checks. The
tested Python and PowerShell helper hashes were reread unchanged. No science,
clock, ledger, phase control, production commit or publication was changed.
