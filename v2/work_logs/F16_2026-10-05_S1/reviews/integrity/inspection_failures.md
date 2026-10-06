# Preserved preliminary inspection failures

Contributor: ChatGPT (GPT-6 Astra Pro), delegated F16 integrity reviewer.
These are read-only inspection errors before the recorded verifier run, not
preparation, evaluation, model generation, frozen-challenge or verifier attempts.
The entries are retrospective descriptions of the tool records; no missing
start time has been invented.

1. **Membership inspection, first attempt; exit 1; tool chunk `d17e49`.**
   The inline standard-library JSON inspection assumed `manifest["files"]`
   was a list in both schemas and evaluated `v["path"]` for each item. F14's
   `files` is a dictionary, so iteration produced strings and raised
   `TypeError: string indices must be integers, not 'str'` at stdin line 4.
   Before failure stdout identified `v2/experiments/freeze.v1.json`, its seven
   top-level keys and `file count 34`. No file was written. The subsequent
   inspection explicitly handled the dictionary and list schemas and completed.
   The recorded audit uses that corrected schema handling and succeeds once.

2. **Reporting-source discovery; exit 2; tool chunk `4b7181`.**
   A combined read command ended with
   `rg -n 'report_sha256|output_manifest|reporting_code_sha256' v2/experiments/F15_v1_analysis/*.py v2/work_logs/F15_ND01_2026-10-05_S1/audit_report_addendum.py`.
   No Python files exist directly in `F15_v1_analysis`, so the unmatched glob
   produced `rg: v2/experiments/F15_v1_analysis/*.py: No such file or directory
   (os error 2)`. The other named source was read successfully. A later bounded
   recursive search located `v2/experiments/summarize_f15.py`, and its registered
   source hash was verified in `source_hashes.json`. No file was written.

Some broad initial text-read output was truncated by the tool display. Follow-up
reads narrowed the relevant sections; no omitted output was treated as inspected.
Neither inspection error prompted any experiment, scientific retry or broad test.
