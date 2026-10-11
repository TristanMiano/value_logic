# P3-10 frozen execution review

Signed by **ChatGPT (GPT-6 Astra Pro)**, agent `/root/freeze_review`, at **2026-10-11T14:52:57.618540+00:00**.

**Verdict: PASS within the reviewed execution scope. No concrete blocker found.**

This is P3-10 validation of the unchanged P3-09-v1 freeze. It is not a P3-11 contribution review. The reviewer contributes **zero principal Research90 minutes**.

## Actual observations

The official read-only `verify` command returned `VERIFIED` with exit code 0 under the required `-E -S -B -X pycache_prefix=/dev/null/value_logic_p309` startup. It reported **no final exposure**. The matching freeze manifest is `69d4d4a84c649698a006bce00a87b0038d5f7d19f2da4e96e6ef3d4e42e37c70`; the base commit observed was `ea3e20dd9889c2ee22141c17390595867d33d8ab`.

A separate direct hash check matched every one of the 50 source records in both the live tree and copied frozen tree: **100 source checks, zero mismatches, zero symbolic source files**. It also matched the runtime, schedule, preparation-check and prepared-method artifacts to their manifest hashes, and matched the preparation receipt to the manifest. No stage was run.

The exact current runtime satisfied the bound Linux, little-endian, x86_64 CPython 3.12.14 record, including the interpreter, 689 supplied standard-library source/extension files and 12 native-closure records. The only recorded missing native dependencies are the two explicitly excluded optional Tcl/Tk libraries. The loaded-source origin and startup checks reject external site modules and source-less bytecode. The preparation receipt and all six recorded preparation check groups report their required successful status.

## Fixed denominators

| Unit | Exact scheduled count |
| --- | ---: |
| Public input groups | 12 |
| Broker paid episodes | 336 |
| Certificate complete histories | 104 |
| Conformance public units | 60 |
| All public units | **500** |
| Private score units | **500**, one for each public unit |
| Aggregate analysis units | 1 |
| Broker request positions | 28,160 |
| Mandatory ordinary identity mirrors | 18 episodes / 1,536 positions |
| Certificate delivery attempts | 416 |

The public schedule has 500 distinct unit IDs and 12 distinct group IDs, with no unit referencing an unknown group. The conformance split is 18 structural and 42 information units. `rows_from_seals` derives its expected unit universe from the frozen schedule and rejects missing, duplicate, unknown or changed units. The denominator does not depend on a result's self-reported count. Incomplete parent episodes or unavailable reports cannot produce positive full-denominator primary claims from a favorable surviving subset.

## Public-before-private boundary

The final entry point first requires a unique in-progress P3-10 chunk and `next_task == P3-10`, then verifies the freeze. Under the writer lock it publishes and fsyncs the exposure marker before the generator callback can receive `P3-10-EXPOSED`. The only final output root is fixed in the source and protocol.

The public stage requires every input seal. Its callback passes the frozen unit, sealed public input and arm configuration to the paid runner. The inspected broker and certificate public paths do not invoke their private truth routines. Certificate witnesses and bounds are explicit supplied tasks; the exposed legacy conformance definitions remain labelled regression/conformance.

The evaluation branch cannot call a private scorer until `public_stage.verify_complete()` and `public_stage.completed()` have verified every public unit. Each evaluation record binds the exact public-result and input-result hashes. Analysis similarly requires every scheduled private-score seal.

## Attempt and failure treatment

The lifecycle writes immutable start, result and completion-seal records. Result and seal publication are separately durable; an orphan result without a seal is incomplete. All seals bind the exact stage identity, schedule, unit, result and start receipt. A missing derived stage index can be rebuilt from a complete valid seal set without rerunning a method.

Each stage admits at most two attempts. The second requires the explicit `unexplained_infrastructure` classification and a concrete nonempty investigator reason. Completed units are verified and reused byte-for-byte. A completed stage cannot be replayed as a retry. Partial and interrupted evidence remains in its original attempt directory.

Typed unavailable service and invalid delivered semantics remain completed outcomes. They do not become infrastructure retry permission. Unexpected exceptions propagate after a preserved failure record; there is no automatic retry. A deterministic defect requires the versioned amendment process specified in the protocol, preserving exposure and the original record.

The outer attempt audit marks lost interrupted public costs unknown. The frozen analyzer retains descriptive completed-path effects while withholding end-to-end positive economic flags when that accounting is incomplete. This prevents an interrupted first attempt from becoming an implicitly free execution.

## Evidence and scope

`review.json` binds every reviewed file by SHA-256 and includes the full source manifest checked. `verify_receipt.json` preserves the exact successful command, tool return code, reported duration, observation metadata and output digest. `verify.combined.txt` preserves the tool's complete returned output. The original tool invocation did not separately capture stderr or emit UTC start/end timestamps; those are explicitly marked unrecorded, not reconstructed. This signature time is the actual preservation time.

The preparation's 13 lifecycle checks were inspected as frozen historical evidence. They were not rerun. This reviewer generated no final input, executed no final stage, changed no frozen file, and changed neither task selection nor the principal clock. No final result or contribution conclusion is claimed.
