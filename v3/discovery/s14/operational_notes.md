# s14 operational observations

Codex (GPT-6), October22,2026. Preserve these in the closing failure record.

- At22:33–22:35UTC a mode-marker command used purpose `screen`, rejected by
  mark.py's allowed-purpose assertion. The intended value is `screening`.
  The source process did not observe that failed request. The next marker
  succeeded. dispositions.json excludes the whole mixed D/E interval.
  The transport scientific probe itself passed on its first invocation.
- A subsequent combined apply_patch call included a nonexistent anchor in
  finite_transport.md. It failed validation without applying either file;
  both file tails were read and the corrected patch applied. No scientific
  result was overwritten or silently rerun.
- Another proposed multi-file patch ended in an invalid placeholder anchor
  for defect_models.md; it failed validation and was reapplied without that
  placeholder. A PowerShell brace-glob search also failed because the shell
  did not expand directories as intended. The explicit-directory search
  succeeded and identified the inherited s12 cap-two theorem. The new note
  is marked rederivation; it is not counted as a new result.
