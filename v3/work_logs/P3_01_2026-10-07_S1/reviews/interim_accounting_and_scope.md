# P3-01 interim accounting and task-scope review

Reviewer: **ChatGPT (GPT-6 Astra Pro), same-model internal sub-agent**.
Date: 2026-10-07 UTC. Nonblind internal review; not an external audit.
This review's own resource time is unmeasured and contributes no additive
principal-clock credit. No canonical records, ledger rows or publication state
were changed.

**Disposition: P3-01 remains in progress.** The accounting below is an interim
snapshot, not a declaration that Research90 or any gate has been completed.

## 1. Snapshot and independently recomputed totals

The snapshot was read at `2026-10-07T01:14:59.976209+00:00`. It contains eighteen
clock events, eight closed raw segments and two dispositions. The last closed
boundary is `2026-10-07T01:14:59.377256+00:00`, monotonic reading
`28868684405256 ns`. A D/R segment begins there and is open; it receives **zero
credit in this snapshot**.

All durations below were reconstructed directly from the JSONL inputs with
integer nanosecond arithmetic and `Decimal`, without using the clock helper's
floating-point minute display as the authority.

| Effective category | Exact nanoseconds | Minutes, decimal display |
|---|---:|---:|
| D | 810520082490 | 13.508668041500 |
| L | 471898798946 | 7.864979982433… |
| E | 209645593235 | 3.494093220583… |
| Research D+L+E | **1492064474671** | **24.867741244517…** |
| O | 273527704507 | 4.558795075117… |
| Total engaged D+L+E+O | **1765592179178** | **29.426536319633…** |
| Recovery excluded from both totals | 193453620971 | 3.224227016183… |
| All closed elapsed time | **1959045800149** | **32.650763335817…** |

Closed research is `1492064474671/60000000000` minutes exactly. The remaining
Research90 requirement at this boundary is
`3907935525329 ns`, or `65.132258755483…` minutes. Subsequent observed work can
increase the total; this review does not estimate or credit it prospectively.

Effective lane time is R `669795484921 ns` and X `822268989750 ns`. Their sum is
exactly the closed research total. O and recovery carry no research lane. The
60/40 lane split is a forecast, and the protocol applies its minimum lane share
over two cycles rather than requiring an exact split at this interim point.

The prior phase-three setup row remains O only: `876.356952516 seconds`, or
`14.6059492086 minutes`. It does not contribute to this task's research floor.
No phase-two research or POST-B-1 balance was imported into the phase-three
floor.

## 2. Corrections CD01 and CD02

### CD01 — mixed administrative interval

The raw D/R segment begins at `00:46:32.791985` UTC. CD01 covers its initial
interval through the existing check at `00:50:09.834020` UTC:

```
27379141161571 - 27162099125653 = 217042035918 ns
```

The disposition changes this interval from D to O, with no lane. This is
`217.042035918 seconds`, or `3.6173672653 minutes`. It remains engaged
administration but supplies zero research credit. Its stated reason is mixed
scientific drafting and planning how to satisfy the protected duration, with
no finer measured split available. Excluding the whole mixed interval from
research is conservative.

The raw segment and original D/R clock event remain present. The correction is
an appended disposition, not a rewritten historical mode.

### CD02 — compaction and restoration interval

CD02 starts at the last observed check before compaction,
`01:09:20.031537` UTC, and ends at the resumed switch at
`01:12:33.484868` UTC:

```
28722792300017 - 28529338679046 = 193453620971 ns
```

It changes that part of the raw D/X segment to recovery, with no lane and zero
engaged/research credit. The entire `193.453620971 seconds` is excluded,
including any unknown summarization gap and the brief restoration read. It
does not attempt to infer how much useful reasoning may have occurred inside
the gap. This is the appropriate conservative treatment.

The following observed O interval, `01:12:33.484868`–`01:13:29.970828`, records
clock/accounting correction work. It is `56.485668589 seconds` of administration,
separate from the excluded recovery. If additional inactive time is discovered
inside that interval, it should receive another explicit disposition; the
present arithmetic does not infer an extra inactive gap.

## 3. Structural and preservation checks

The independent reconstruction checked the following:

- Every closed duration equals its end monotonic reading minus its start, and
  is positive.
- Raw closed segments are contiguous and do not overlap.
- Events are strictly ordered in monotonic time and use the same runtime.
- The runtime is `linux-P3-01-S1:e16f10d3-6414-4e6b-a384-e9b4ddea7ee9` throughout
  the inspected events, segments, dispositions and open state.
- Both disposition endpoints match actual clock events, including their UTC
  values; each lies wholly within exactly one raw segment of its original mode.
- CD01 and CD02 do not overlap.
- Reclassification preserves total elapsed nanoseconds exactly.
- The open state's start is the last closed endpoint; it is not added to
  completed totals.
- Observation gaps in the snapshot are well below fifteen minutes, including
  the interval later excluded for compaction.
- Baseline hashes and byte counts for all ten listed repository files match
  the bytes at source commit `6ec18182e7bd3d90bf33546e731b669a2a2ff9fe` and
  their current bytes. This includes both ledgers, the phase-two paper/TODO,
  root README, phase-three planning files and the Gate D snapshot.
- The prior 435 bytes of `v3/time_ledger.csv` are preserved exactly, including
  the setup row. The ledger has not yet gained a P3-01 row.
- The `276313` bytes of `v2/time_ledger.csv` still have SHA256
  `5c71a4727f1cb7e03565f1c495b0c63b351863583120f0ec5684aca48bd122c6`.

The clock helper appends observations/closed segments and applies dispositions
when reporting effective segments. Its conservation assertion is appropriate.
The independent checks above additionally verified ordering, adjacency,
runtime consistency and event anchors on this actual dataset. The helper's
reported decimal minutes use floating point; final threshold and ledger
arithmetic should continue to use the stored integer nanoseconds.

### Preservation boundary

The baseline provides a strong byte-for-byte comparison for the prior tracked
files. For new clock files, the current raw records retain their original modes
and corrections are visibly separate. The helper's append behavior and the
data's consistency support that preservation claim. Without an earlier saved
hash of every raw prefix, this review cannot independently prove that no
pre-snapshot byte was ever changed. The following snapshot hashes make that
boundary inspectable going forward; clock state is an intentionally replaced
current pointer rather than an append-only log.

| Snapshot file | Bytes | SHA256 |
|---|---:|---|
| `clocks.jsonl` | 5251 | `0c5fcace4d353a88f5b45a3488aa22411724ac8829e218b3aebe24dc4e2e09c5` |
| `segments.jsonl` | 3327 | `520e40f4056b1e88e0a0742acde7b84ad13c5c598b9b36671261aff28a5d0d70` |
| `clock_dispositions.jsonl` | 1096 | `0fc5df26bc9e9d7ca80747fca8d0a85b4aa42239ac124912e61a2b759194b586` |
| `clock.py` | 5920 | `d36994e2172341908d61718c3e34b3bc5b29e5eb333bc05e0cbc1d09999e7db7` |
| `baseline.json` | 2075 | `6af8b4f959673927831a961f28f73e42d6deafca8ce8b3c5d5284339de5b3c29` |

The observations describe principal work only. No field or ledger row adds
concurrent reviewer minutes, and reviewer outputs explicitly retain separate
or unmeasured resource status. Arithmetic consistency cannot prove continuous
engagement from timestamps alone. The principal must still disposition any
known unattended waits, inactivity or unobserved intervals; the absence of a
wait row is not independent evidence that none occurred. This limitation does
not alter the exact reconstruction of the currently recorded categories.

## 4. P3-01 evidence targets versus current artifacts

The relevant target is the P3-01 paragraph in `TODO_v3.md`, not the later
representation gate, learning implementation or final experiment.

| P3-01 target | Current evidence | Interim assessment |
|---|---|---|
| Relevant phase-two interfaces reconstructed | Main contract §2; inherited-interface review; paper/core and reflection pointers. | Present with correct scoped inheritance. |
| Selected primary definitions reconstructed | `v3/literature/01_source_contracts.md` and linked induction, expectation and counterfactual source notes. | Present as selected definitions/statement imports, with retrieval limits and nonblind review disclosed. This review does not independently recheck every external theorem. |
| Formal language and theory | Main contract §3 specifies encoded arithmetic, versioned c.e. theory/checker and bounded-program query schema; axiom admission and investigator timeout distinctions are explicit. | Appropriate parameterized contract. A concrete VM and full algorithm belong to later implementation. |
| Observation/proof stream and update timing | Main contract §5; interpreted answer versus theorem receipt in U02/U04; pre-resolution forecast separated from final decision report. | Present. Does not grant full logical closure or future labels. |
| Computation budget and task loss | Main contract §6 and O-COMB; loss/resource accounts and paid reasoning service. | Present at interface level; add compact resource/input closure fields from the resource review before treating the contract as operationally complete. No numerical budget freeze is needed in P3-01. |
| Five uncertainty objects separated | Main contract §4 distinguishes truth, proof production, model adequacy, axioms and usefulness; action availability is explicitly a constraint. | Present. |
| Exact duties and comparisons | `01_desiderata.md`, main contract §§8–9 and source locators. | Present. The combined ordinary baseline receives joint information, model plurality, paid computation and provenance. |
| Separating examples | Twelve canonical examples plus cost-criterion probes and finite checks. | Present; exact finite checks remain development and do not implement every claimed future service. |
| Improvement, equivalence and failure for all five questions | Main contract §9. Q3 now explicitly requires a logical-query benefit rather than a scientific approximation example alone. | Present at the intended prospective scope. |
| No carrier selected only for real-valuedness; no universal assumed ability | Open shortlist in §10, explicit exact-recoding probe, NOT YET SUPPORTED P3-N01. | Present. No gate or later task pass is claimed. |
| Protected Research90 | Closed research at the snapshot is about 24.868 minutes. | **Not met. P3-01 remains in progress.** |

## 5. Remaining concrete scope corrections

1. **Resource and input closure.** Bring the compact field requirements from
   `resource_information_stress.md` into a canonical contract section or an
   explicitly incorporated appendix. Name the primitive machine/cost model,
   exact readable fields, precision/encoding, admitted libraries/advice/caches,
   postprocessing and selection-cohort record. Their eventual concrete choices
   can remain prospective. This closes “same budget/information” as an auditable
   requirement without beginning implementation.
2. **Stale warrant option.** Desiderata R01 still says every dependent warrant
   must be rechecked or transported. Add the already established option of
   marking it stale/unusable until paid rechecking is possible. Otherwise it
   can read as an immediate unlimited recomputation obligation, unlike U04.
3. **Finite-fragment qualifier.** U03 should say it respects every selected
   Boolean constraint *represented in the declared finite fragment*. Its
   common notation allows `C_t` to include broader checked material while
   `W_t` represents only a selected fragment. This small qualifier avoids
   reading local coherence as respect for all unprocessed arithmetic facts.
4. **Evidence-to-obligation map.** At completion, identify which review issues
   were corrected, accepted as limits, or deferred to their already named
   downstream owner. Do not copy a raw review's earlier “missing file” comment
   into a current blocker after the companion artifact has been created.

The earlier substantive concerns about conditioning on zero-probability events,
theory proofs versus interpreted answers, bounded-horizon timeout, Q3's logical
target and pre-resolution scoring have been addressed in the current canonical
draft. They do not need another recurrence of the same work.

## 6. Completion boundary and recommendation

Continue meaningful P3-01 work and record it under the existing clock. The
conceptual contract is substantially assembled, but the protected floor is
still unmet at this snapshot. More evidence can strengthen its assumptions,
counterexamples and comparison/operational closure without implementing the
P3-02 representation theorem or the P3-03 learner.

At the real task boundary, close the principal interval, apply all known
exclusions, compute exact actuals, append rather than replace ledger history,
and synchronize the work log, TODO pointer and claim status. Preserve the
original forecast and explain the actual mode split and whether the floor was
useful. Mark the task complete only when both evidence and Research90 are met.
P3-02 and all gates remain unstarted until separately selected. This review
makes no advancement or publication decision.
