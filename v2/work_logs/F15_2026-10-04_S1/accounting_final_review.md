# F15 final accounting: independent saved-record review

Contributor: **delegated ChatGPT (GPT-6 Astra Pro), execution audit**, with a separate delegated integrity check. This review is an **uncredited administrative tail**: zero minutes are added to the principal's E60, engaged total or POST-B-1 clock.

## Result

**Passed: 775 independent accounting checks, zero failures.** A separate delegated read-only inspection also passed **65 integrity checks**. The recorded final actuals and ledger agree with the raw monotonic endpoints, all current exclusions and the preserved mode reclassification. Neither reviewer executed or imported the finalizer, issued a clock command, modified the ledger or raw records, or generated experimental data.

The reproducible review calculation is [accounting_final_review.py](accounting_final_review.py). Its saved [machine result](accounting_final_review.json), including raw-input hashes, exact integer arithmetic, accounting transfers and check counts, has SHA256:

`ac13ad4be9b14c68c6f44f0979f2e42663b6de96696d0c98f0eacfa6434af7f5`.

The review script writes only its own exclusive result; it does not overwrite an existing review. Its source hash is bound in that result. The saved result and its sidecar were flushed/fsynced, with directory fsync and an exact output reread.

## Independent arithmetic

The review first reconstructs the 43 segments from the raw clock transitions, ignoring observational `check` events. It sums the original mode durations directly from **integer nanosecond endpoints**, then transfers the recorded wait, recovery and reclassification quantities between those raw mode totals. This aggregate-transfer calculation is separate from the serializer's effective-row construction. A second calculation reads and checks every appended CSV row, including its original endpoints, classification, credited time and exclusions.

All 43 segments are contiguous and nonoverlapping, from **2026-10-05 03:42:04.985965 UTC** to the explicit stop at **05:09:37.119388 UTC**. The final clock state is null. The observed wall span is **5,252,133,424,729 ns**, or 87.53555707881667 minutes, and equals the exact sum of engaged time, observed wait and excluded recovery.

| Quantity | Exact nanoseconds | Minutes, displayed |
|---|---:|---:|
| D | 0 | 0 |
| L | 0 | 0 |
| E / research | 3,605,453,176,091 | 60.090886268183 |
| O | 289,495,001,776 | 4.824916696267 |
| Total engaged | 3,894,948,177,867 | 64.915802964450 |
| Observed wait | 13,119,968,039 | 0.218666133983 |
| Recovery / conservatively excluded unobserved intervals | 1,344,065,278,823 | 22.401087980383 |
| Research lane R | 1,518,078,799,527 | 25.301313325450 |
| Research lane X | 2,087,374,376,564 | 34.789572942733 |

The strict E60 requirement is **3,600,000,000,000 ns**. The independently recomputed E total exceeds it by **5,453,176,091 ns = 5.453176091 seconds**. No rounding of a displayed minute total is used to establish the floor. D/L/O, wait, recovery, parallel agents and administration after cutoff contribute no E credit.

All three conservative recovery exclusions, the single observed-wait adjustment, the explicit artifact-recovery wait segment, and the E/X-to-O reclassification are applied. The second recovery record contains `386.43922806200004` seconds. Normalizing that serialized number to the clock's nanosecond resolution changes it by only **−0.00000000000004 seconds**; the adjustment is recorded explicitly in both actuals and this review. No substantive negative duration is clamped, and every per-segment and aggregate conservation identity holds.

The exact engaged addition is **64.91580296445 minutes**. Adding it to the preserved **636.727190-minute** POST-B-1 entry gives:

- **POST-B-1 close:** 701.64299296445 minutes.
- **Remaining to 960 minutes:** 258.35700703555 minutes.
- **Inherited earlier eight-hour overshoot:** 54.976816 minutes, unchanged.
- **Recurrence-clock reset:** none.

The immutable initial forecast remains central D10/L0/E90/O20 = 120 engaged minutes; high D20/L10/E180/O30 = 240; waits 5/20; research-lane forecast R/X 60/40. Source revision remains `5388a3f9b0f18ad4f4e33d7e0cd04ea38f03e43e`. The finalizer's recorded launcher starts after the accounting cutoff and reports one successful attempt. Its own administration is outside the credited clock.

## Historical ledger and output integrity

The original **203,501 bytes and 906 data rows** are intact. The new **14,275-byte append** is identical to the CSV bytes preserved in `finalization_intent.json` and contains exactly **43 F15 rows**. There were no earlier F15 rows. The complete ledger now has **217,776 bytes and 949 data rows**.

| Object | SHA256 |
|---|---|
| Original ledger prefix | `7f777f89e0aff82d58752d0b1774c30e015fe9f3dbbf4faa1caae9b35c49988f` |
| F15 append | `2af989da6296e077ef3afe6826ddc2aadbd08f487715eec0e0d93842daa8dd3d` |
| Complete ledger | `44c93cc930fdea2d588f663688e71615a84b32f98517eadd4bab3943efa154bd` |
| [actuals.json](actuals.json) | `4633b7fdaee65831ed5f58ba36767453e125fd122ff8de89d4d0f3a359eb29ec` |
| [ledger_integrity.json](ledger_integrity.json) | `d672c96a9972c4e6de378af3e22421012957271845865e0d329965ecbfb295f7` |
| [finalization_intent.json](finalization_intent.json) | `63dcf359aab6fe12fc309b5eabcb5e153143353fd21bd11e0ff76bbc1a112bc1` |

All three accounting-output sidecars validate. All nine raw-input byte counts and SHA256 values match the files bound by final actuals. The additional delegated integrity check also compares those hashes across actuals, integrity and intent, and confirms that saved actuals equal the intent's planned actuals under the recorded serialization. The recorded serializer hash matches the statically reviewed file.

## Scope

This review verifies the arithmetic and integrity of the preserved timing observations and operator classifications. It does not invent a historical activity trace, infer the duration of an unobserved interruption, or add concurrent work. It does not assess the E60 floor's usefulness on the principal's behalf, establish a scientific/contribution claim, start F16, or grant a Gate C/D pass. Final document consistency, commit hash and actual push outcome remain the principal handoff's responsibility.
