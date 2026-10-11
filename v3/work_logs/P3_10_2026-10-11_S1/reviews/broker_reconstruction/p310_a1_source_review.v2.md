# P3-10-A1 driver source review: v2 closure

Contributor: **ChatGPT (GPT-6 Astra Pro)**, agent `/root/freeze_review`.
Signed UTC: **2026-10-11T15:33:00.186907+00:00**. Reviewed source SHA-256: **0e6fa551fe78561026972e5ba7e83e810927b8778c65bfa8c88e607c85b49cca**.

**PASS_SCOPED. Both gaps in the preserved first-draft source review are closed. No remaining blocker was found in this revised driver scope.**

The revised `inherited_rows` explicitly requires the original input/public schedule files and original input complete index to exist before inherited stage helpers run. Each original schedule is compared with its exact expected identity, schema and units before the corresponding helper is used. The public helper now uses `completed(require_all=False)`, which rejects unexpected original unit directories. Under the old writer lock these operations compare existing records and cannot take the previously identified schedule-reconstruction branch.

The original verifier subprocess now receives an immutable raw outcome receipt immediately after return, before a nonzero exit or malformed stdout can raise. That receipt includes argv, cwd, start/end UTC, return code, stdout and stderr. The separate successful verification receipt and single-command-per-stage behavior are retained.

The diff changes only these original-root guards and verifier-receipt preservation. The reviewed 440+60 composite public barrier, 12 original input references, new amendment binding, unchanged 500-unit score universe, inherited bootstrap placement, explicit provenance and merged unknown-prefix accounting remain unchanged from the first source review. The orchestration/original lock composition still avoids reacquiring the same writer lock around the inherited executor.

This conclusion concerns source only. It does not certify a future manifest, source snapshot, development result or amended stage outcome. The old v1 public stage remains failed; amended conformance and mixed-provenance orchestration remain explicitly post-exposure. The original unknown prefix keeps complete end-to-end economic accounting false.

The exact v1 and v2 source snapshots and narrow diff are preserved in this review directory. No frozen/live source was edited, no final payload was read, and no driver, worker, scorer, generator, official verifier or observer was executed by this review. The main broker observer remains unchanged. **Zero principal Research90 minutes** are claimed.
