# S07 publication verification

**ChatGPT (GPT-6 Astra Pro)**. Repository maintenance; zero research credit.

[The machine receipt](checks.json) records the actual local publication checks.
Research results and the closed clock are described in [cp01](../cp01.md).
Verification does not promote S28-B1 or assign economic benefit to unpriced
resources. Frozen scientific code, source, receipt and prior clock bytes are
preserved. The new raw acquisitions remain DEVELOPMENT.

The publication runs use a separate Python 3.13 verification environment with
the current CI dependency pins and CMake available for native-kernel checks.
The [reproduction guide](../reproduce.md) gives the commands and explains which
scientific commands would acquire new evidence. The publication gates do not
rerun those source acquisitions. Actual local outcomes and remote workflow
status are reported separately.

## Local outcomes

The [full suite](full.txt) passed **1,728 tests with no skips**, including the
native-kernel cases: 162.441 seconds reported by the runner and
164.758350825 seconds observed for the subprocess. The final mathematical
Markdown and local-link gates passed; portability regressions passed 24 tests;
relocated evidence and the 230-file handoff inventory verified. Staged path
limits and whitespace were checked after final formatting.

The initial math finding was one unsupported macro in a new active note. The
initial whitespace gate found four extra EOF blank lines in new narrative
notes and a CRLF ending on the new administrative ledger notice. The
[formatting record](formatting.json) gives the exact changes; no acquired
scientific source, proof, result or raw clock observation changed. The
[initial whitespace receipt](whitespace.json) preserves its failed output
losslessly in a compressed log. A receipt-assembly field-name error occurred
after all gate commands completed; the aggregate receipt records that
administrative error and was rebuilt from the saved command receipts.

The full suite ran during final dashboard assembly. The later standalone link
and math gates cover the completed dashboard; its
[preservation check](dashboard.json) verifies all seventeen historical row
objects and Markdown rows plus the new exact cumulative sum. Final EOF-only
formatting changes alter neither formulas nor link destinations.
