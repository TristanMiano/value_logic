# Final bounded scope-consistency review

Contributor: ChatGPT (GPT-6 Astra Pro), 2026-10-09 UTC. R-P3-B-A.
Same-model, nonblind independent audit. **Zero principal clock credit.**

## Verdict and reviewed extent

**PASS; no remaining blocker in the reviewed extent.** I checked the complete
main derivation through **§§1–13 and numbered equations (1)–(16)** against the
completed proof and source reviews, saved uniform and adaptive results,
registry transfer, signed resource audit, setup-scope erratum, and preserved
archive failure/correction/readback records. No policy, scientific experiment,
implementation probe or archive rebuild was rerun.

The exact reviewed source is `v3/derivations/07_selective_feedback.md`:

- Initial snapshot SHA-256:
  `c62cc840cf35af4419a64234ab49c5ed651400b1bd7f1023003fa77cb1b5e401`.
- Corrected snapshot SHA-256:
  **`697bed3f7b63e0b216bf7a82492e783bea383b69ff73e0b9cdd6020852a8c45a`**.

Both snapshots and their narrow diff are retained. The root made the two
documentation corrections described below; this reviewer made no main-file
edits. **Any later observable-performance companion or appended link is
outside this receipt.** That separate work has its own owner and review.

## Numbered mathematics and integration

| Equations / section | Disposition |
| --- | --- |
| (1) | Correct pathwise Prod potential and stated `eta<=1/2` scalar inequality. |
| (2)–(4) | Correct frozen-block uniform averaging, `B-1` paid-action correction, fixed full-tape comparator, and `K=max(2,B-1)` regret allowance. The constant-in-horizon statement is confined to the ideal rule and explicitly distinguishes the corrected comparator. |
| (5)–(7) | Correct positive fixed-mass normalizer, one-sided posterior inequality, state allowance `(B-1)mK/(2^s-1)`, action allowance `(T-m)2^-h`, and exact bit count. The separate 95-bit extraction transient and the `N=4,h>=s+2` exact-grid exception agree with source. |
| (8)–(9) | Correct all-in expectation and sufficient economic condition. Paid child invoices are counted once; failed execution does not receive the success theorem; expected task loss remains separate from the funded pathwise expenditure cap. |
| (10) | Correct all-issued Brier factor `B`, fixed-state term `BmK/(2^s-1)`, and `2T2^-h` scalar-rounding term. No retrospective correction of purchased forecasts is implied. |
| (11)–(13) | Correct adaptive remaining-action estimator, second moment, probability-floor condition, `HK` allowance, implemented ticket factors and conditional expected paid-fee identity. Full public-block lookahead and the truthful trusted-broker boundary are explicit. |
| (14) | Correct adaptive Brier allowance `L*+HK log N+HmK/(2^s-1)+m+2T2^-h`, clipped at `T`. It does not reuse uniform averaging or add action rounding twice. |
| (15)–(16) | Correct source-level common-unit-price obstruction: shared admission plus expert cost `+9`, table lookup `+10`, and learner close checks `+12` yield `11T+purchases`. Current cold constants are 4,908 for uniform v1.2 and 8,809 for adaptive. |

The exact-log refinement in §3.3 agrees with the independent 20-certificate
audit: the existing rule receives a sharper comparator coefficient, without
changing its actions, state allowance or invoices. The general learning-rate
option in §12 is correctly labeled unexecuted and retains the new-denominator
capacity warning.

Section 8 correctly obtains `L*<=T/2` from the two constant experts and treats
it as a source-known upper bound. Its `3T/8` and `T/2` statements deliberately
refer to the conservative uniform theorem; §3.3 separately supplies the
sharper source-known certificate. The scalar resource-price cap uses either
the common price or the maximum nonnegative category price, preserving units.
The full pathwise loss cap uses `c(T-m)`, not the smaller expectation envelope.

The precision lower floors, greedification counterexample, fixed/adaptive
environment boundaries, and loss-reducing sound-answer override match the
earlier reviews. The override does not authorize changing the scheduled
purchases or raw updates. Weight-state size is distinguished from the entire
bit tape, request tape and output history. P3-08 remains future work.

## Economic and provenance crosscheck

`scope_saved_record_crosscheck.json` binds the supporting files and records a
read-only arithmetic crosscheck. The main tables reproduce the saved results:

- Uniform `T=3968,B=8` current cold costs are **2,935,924** for exact weights
  and **1,039,136** for fixed state, explicitly derived by adding **26** registry
  units to the observed v1.1 costs. Errors remain 1,703 and 1,702. The 64.6%
  representation saving and observed 1,342-to-18-bit change match the records.
- The adaptive row is an actual core-v1.2 observation: **1,382,703** units and
  1,754 errors. Its purchased-fee reduction of 8,227 units and total increase
  of 343,567 units are correct comparisons with the current uniform transfer.
- All four 3,968-round exact-control totals match the saved results, including
  the table's **171,880** cold units and zero errors.
- The Brier scores and conditional action means in §10.1 match their exact
  rational records. All six inspected adaptive/matching-uniform Brier scores
  exceed `T/4`. The prose correctly distinguishes conditional means along a
  selector path from the theorem's unconditional expectation.

The v1.1/v1.2 disposition is explicit and correct. Successful source operations
are unchanged by the exception-only guard, but source registry bytes cost 26
more units; the document does not call the transferred costs new observations
or transfer physical runtime. Adaptive runs actually use the current core.

The setup erratum is represented accurately. Excluding both registries leaves
the table's 1,611 construction units, covered by `11T` at `T>=147` (first legal
even horizon 148). Waiving all learner setup while charging the complete table
requires 14,088 units and `T>=1281` (first legal even horizon 1,282). The saved
992-round minimum purchased bill 17,510 gives the stated **14,334** positive
margin; it is correctly confined to saved paths. The signed `cache` difference
of **-11,408** prevents a coordinatewise price-dominance claim. The optional
24-unit equal-emission surcharge cancels the previously dropped 24 learner
output units per round algebraically and is correctly labeled unexecuted.

The table is funded over the stated horizon. A conservative source envelope
is `1611+74T` units and `1611+9T` meter events. At `T=8192` these are 607,819
units and 75,339 events, below its 10,000,000-unit and 100,000-event capacities.
This is a source-cap check, not a new table execution or hardware estimate.

## Historical archive disposition

The main note preserves the evidence through its linked analysis. That
analysis accurately reports the failed deletion guard on a 3,029,601-byte
truncated prefix, retention of intact originals at that failure, repair to the
expected 3,105,040-byte archive, and verification before removing redundant
raw originals. The correction records retain the historical v1 size error;
manifest v2 is authoritative. The later readback reports 99 verified payloads.

The linked account leaves the causal origin **unknown** and says no scientific
run was repeated. It does not claim that the historical incomplete archive
was a valid complete file or erase its failed guard. My check reconciles the
saved receipts; it does not claim another independent payload revalidation.

## Findings resolved during this audit

1. The initial §3.3 implied that a one-expert endpoint could be executed by
   the current service. The root now calls the endpoints mathematical checks
   and states that `execute()` fixes the four-expert library.
2. The initial §11 linked measured construction cost and actual invoices only
   to the pre-implementation design. The root now links the correctness
   argument to that design and the charges/invoices to the executed result
   and its analysis.

The saved diff contains exactly those two repairs. They change no theorem,
implementation, experiment, price record or historical evidence. The
accompanying scope manifest binds the final reviewed document and receipts.
