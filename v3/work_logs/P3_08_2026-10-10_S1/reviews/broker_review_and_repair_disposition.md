# P3-08 broker review and authorized repair disposition

Contributor: **ChatGPT (GPT-6 Astra Pro)**, integration-review sub-agent,
October 10, 2026 UTC. **DEVELOPMENT** only.

**Disposition:** the inspected generic broker preserves the inherited
numerical process and supports the selected live hard-correction interface.
Seven concrete API defects found by the first executable review were repaired
under the principal's explicit delegation. The repaired source passes all
15 focused cases. One additional first-run failure was a mistaken test
assumption about reservation headroom, not a source defect; that failure and
the amended test remain visible.

The initial reconstruction and tests were independent, **same-model and
nonblind**. I authored the delegated repairs, so their rerun is correctly
described as **self-check of reviewer-authored fixes**, not a second independent
implementation review. Agent costs and elapsed time are unmeasured; no
principal-clock, overlapping or historical research credit is claimed.
Temporary ownership of `v3/experiments/p308_broker.py` has been returned to
the principal. This report authorizes no commit, push or P3-09 evaluation.

## 1. Preserved evidence and source boundaries

Both runs use copied source closures with the original relative import
layout. They do not import changing live files after their snapshot.

| Item | Initial review | Repaired review |
|---|---|---|
| Directory beneath this `reviews/` directory | `broker_initial/` | `broker_repaired/` |
| Broker SHA-256 | `46057143dd9737b42641240d73c2e277aa1823e3aba627a6d574d07661f588e2` | `399080c950a48c1cd935efbee8ed7769a7af54b7afa14859b5671397638e2e4d` |
| Check script SHA-256 | `fb9aecf608ad17b69a8c6b2fd2f53f3c7ccd6bf4248a1cff6a87bbc222062f08` | `4628b94de7654f3a830c3e998b8d39ef5eabf78b035d6327938dc23bc94d99ed` |
| Results SHA-256 | `7bc0c667a1a60a08bd1bf2010ff210c1590394dd31dcc9f04ee881bee0dd5a9f` | `ec774da157f57a68599112e8640ec6ca6995f44586e30480230ddc2b04a3d48d` |
| Observed start UTC | 2026-10-10 16:20:34.532452 | 2026-10-10 16:23:35.914472 |
| Observed finish UTC | 2026-10-10 16:20:34.573673 | 2026-10-10 16:23:35.958516 |
| Cases | 7 pass, 8 fail | 15 pass, 0 fail |

These timestamps are execution evidence, not an engaged-research ledger.
Each directory contains its prospective `plan.json`, copied sources,
`check_broker.py`, `results.json`, and the targeted history, withdrawal and
post-completion observations. Commands from the repository root were:

```text
python v3/work_logs/P3_08_2026-10-10_S1/reviews/broker_initial/check_broker.py
python v3/work_logs/P3_08_2026-10-10_S1/reviews/broker_repaired/check_broker.py
```

The repaired broker identifies itself as `p308-program-broker-v1.1`. Its
common dependency has SHA-256
`4928a5b9c80e05b497bd93116957139252c65f393e6e12ea4c7ad4727f300a29`.
The initial CNF snapshot has SHA-256
`e69773ef2a9449bc8d36e856c15854409b10f45ef9f263c30ab744c8bf95af47`;
the repaired-run CNF snapshot has SHA-256
`1eb1b7b4faa482e68393bf6b550f3b7faee683f8691b59eae59fd0274bba7f86`.
The subsequent CNF hash
`46fd3e82505b9b6af9805836a562f2f78a3436384e0b3476c4f85cec355817a2`
differs from the repaired snapshot only in its introductory description of
the checked simple-UNSAT certificates; that difference is not a numerical
or tariff change. Dependency hashes for all inherited modules are in each
manifest.

Before the executable snapshot, I also reported static gaps in the original
funding admission and scope-generation handling. The principal repaired them
before `broker_initial` was captured: full-key reads now cost
`32 + 8 * key_words`, hard funding requires enough capacity for every quota
purchase, and invalidated generations cannot revive merely by returning to
an old scope label. The principal retained earlier development versions.
Those static observations are not counted as executable failures of the
captured initial source.

## 2. Seven source defects and one test correction

| Case | Actual initial failure | Repair/disposition |
|---|---|---|
| `withdrawal_when_unfunded` | A denied paid invalidation left the broker active and its completed-episode success warrant intact. | Prepay a terminal failure slot at construction; mark the epoch failed before attempting invalidation. A denied or malformed withdrawal cannot permit further issue/close or a successful current record. |
| `malformed_solver_typed_failure` | The CNF service's distinct `Rejected` class escaped `execute`. | Catch the source service's declared rejection alongside broker rejection and budget exhaustion; retain a typed failed result and paid work. |
| `malformed_query_typed_failure` | The first query's attributes were read before checking the exact query type, causing `AttributeError`. | Validate the contract and every immutable public query record before reading the first query's scope fields. |
| `state_none_admission` | The inherited contract admitted `state_bits=None`, while this fixed-state port uses integer shifts and needs a positive finite precision. | Add explicit exact-integer precision admission in `[1,32]`. |
| `scope_type_admission` | A list-valued epoch reached the conflict set and caused an unhashable-type exception. | Add a paid bounded three-label scope boundary: exact strings, nonempty ASCII, length at most 128. |
| `history_detachment` | A previously returned report changed during ordinary subsequent execution; returned rows also exposed retained mutable records. | Return detached audit copies of rows and complete records. Issued forecast values remain immutable and retained values cannot be mutated through a returned record. |
| `completed_block_boundary` | A second `begin_block` after the declared horizon prepared advice and consumed work before exhausting bits, leaving an open buffer. | Reject at the horizon before preparation; `issue` also checks the horizon. Success additionally requires quota updates, clean buffers and the complete fixed bit count. |
| `failures_and_funding` | The test assumed the final actual bill alone was enough to fund a rerun. It failed at an intermediate provider reservation. | This is a test defect. Reserve headroom is needed even when the final actual child cost is smaller. The amended limited-success check adds the largest provider cap to the observed final bill, still remaining below the all-path episode cap. The original failure is preserved. |

Paid scope validation charges before inspecting its bounded shape and label
contents. The broker's terminal fail-closed status is prepaid for direct
broker callers as well as `execute` callers. Withdrawal does not pretend to
have paid for overwriting old hard entries when its invalidation debit is
denied: it ends the broker's statistical authority first. The retained
historical evidence can remain readable without being a live warrant.

## 3. The inherited numerical component is preserved

`NumericProd` reuses the inherited paid addition and fixed-mass rounding
methods. The generic query boundary, receipt ownership and selector loop are
new. Advice is an exact tuple of declared binary expert outputs. The numerical
forecast is the same integer mass ratio on the same fixed-state weights.

For uniform selection, the recurrence uses the inherited denominator
`k=max(2,B-1)`, applies the selected expert loss once, and rounds back to the
same fixed mass. The check compares new numerators, actions, weights after
each block and total bit use with the old `FrozenProd`, at state precisions
1 and 16. Labels and advice are obtained from real CNF services, then privately
paired with old-service mathematical queries having the same binary label
for this numerical comparison. That pairing is evaluator work. It does not
claim that the old service ran the new CNF tape as a policy.

For ticket selection, the owned law gives multiplicity B+1 to the favorite
position and 1 to every other position, over 2B tickets. The new update uses
the corresponding inverse-propensity factor. Direct comparison with the old
`AllocatedProd._end_block` covers both multiplicities 1 and 5 at B=4 and
state precisions 1 and 16, with exact equality of all normalized weights.
Manually installed feedback in this test is explicitly a numerical check,
not an independently executable receipt interface.

The public broker itself owns its selected ticket and the exact issued
object. A repeated begin at an open block, a freshly forged equal-valued
issued object, and a duplicate close all reject. Callers cannot choose a
more favorable selected receipt after seeing the outcome. Repeated public
query IDs do not weaken this ownership; the pending-object identity and
complete semantic-key binding are separate checks.

## 4. Live hard correction preserves the base path

Real CNF runs with hard correction enabled and disabled use the same seed,
selector, labels, base forecasts, base prospective and terminal actions,
numeric updates and complete bit count. Corrections change only the live
emission and terminal path for a previously checked current key. An explicit
same-block trace selects the first repeated false query: its base and emitted
numerators are both 10 over 16; the later repeated query retains base numerator
10 but emits numerator 0 after the receipt is admitted.

The observed eight-query coupled examples are small development witnesses:

| Selector | Base Brier | Live Brier | Base terminal errors | Live terminal errors | Base paid total | Live paid total |
|---|---:|---:|---:|---:|---:|---:|
| Uniform | 181/64 | 25/64 | 3 | 0 | 5929 | 6476 |
| Tickets | 25/8 | 25/64 | 3 | 0 | 6459 | 7006 |

These values demonstrate exact coupling on those paths. They establish no
population advantage, calibration or confidence coverage. In particular,
there is no free improvement in resource cost: hard lookup/admission work
is charged and the live runs cost more.

The current truth interval changes only on a checked current receipt.
Contradictions are stored as conflicts; scope mismatches and obsolete
generations are stale. A return to the old scope label does not resurrect
the old generation. Pending receipt state is distinct from checked truth.
Issued base and live forecasts remain fixed even when the post-close truth
coordinate becomes exact. The separate translated-performance lemma is
needed for any two-sided live report; the broker alone does not re-prove a
lower bound by recomputing a live mask.

## 5. Receipts, capacity and resource failures

Receipt admission requires the exact local provider receipt class, the
issued query ID, the complete semantic key, successful status, `checked is
True`, an exact binary integer answer, and current provider identity/version.
Focused checks take real local receipts and perturb each bound field; the
broker rejects incorrect query ID, semantic key, provider, version, status,
check flag, answer 2 and Boolean answers. This is validation of an owned
local service boundary, not authentication of externally supplied objects.

The selected provider receives a reserved cap. Its actual resource invoice
is absorbed into the parent meter even when the child cannot return a sound
answer. A provider limit of zero yields a failed broker with no checked
purchase and total paid work 3145. A hard capacity of zero can fail after a
sound answer has already been purchased: the record retains that acquisition
and its paid cost, but no hard entry is created and the full quota theorem
does not become eligible. The repaired check observes total 3454 for that
capacity failure, including 305 child-service units.

The metering model is the declared bounded word tariff. Actual Python CPU,
heap allocation and JSON evidence serialization are not being equated to
those deployment units. The generic source registry, deployment output-word
tariffs, provider invoices and evaluator export must stay distinct. The
main source closure and reporter must be procured and billed separately.

## 6. The all-path funding claim is stronger than one completed run

The broker's advertised bound is a shape-only sum of the largest public cold
service cap in each block plus

```text
4096 + 10 * random_bits
  + T * (EXPERT_CAP + 8192 + 64*N*(z+1)^2
         + 12*(K+1)*(Qmax+32)),
```

where z is the word bound on the declared numeric operands, K is at most
min(hard capacity, quota), and Qmax is the largest admitted public key size.
The selected-label truth and realized cheap invoice do not enter this
pre-execution calculation. Source procurement and the separate reporter
are outside it and must be funded in the combined system.

The load-bearing margins are reconstructable for the captured CNF service:

* At most one provider invocation occurs in each block, and the maximum
  public cap for that block funds any selected position. Provider soundness
  and its advertised service-cap proof remain delegated service obligations.
* There are at most three hard lookups per position. Each scans at most K
  retained entries and pays at most `4 + 2*Qmax` per full-key comparison.
  `12*(K+1)*(Qmax+32)` per position dominates these comparisons and the
  accompanying bounded lookup bookkeeping.
* The finite contract has N<=32, B<=1024 and action/state precision<=32.
  Its conservative operand bound is at most 110 bits, so z<=2. Fixed-state
  additions, divisions, updates and mass rounding fit comfortably within
  `64*N*(z+1)^2` per position. The code does not grow rational denominators
  recursively across the horizon.
* The CNF key has at most 343 words under its 128-character source-label
  bound. The per-position 8192 allowance covers the paid funding scan,
  retained query keys, current scope and output records, receipt checking,
  bounded score/cost calculations, and fixed control overhead. Expert
  execution has its own advertised `EXPERT_CAP=8192`. The maximum-shape
  expert probe observes 4800 units, and inspection of the bounded clause
  and literal loops leaves substantial margin below the advertised cap.
* The initial 4096 allowance and ten units per declared random bit cover
  finite tape initialization/generation/admission and the fixed boundary
  records under the inherited tariff.

This is a conservative bound for this concrete trusted service contract.
It does not certify any arbitrary Python module merely because it supplies
attributes with the same names. Finite tests exercise the arithmetic and
admission boundaries; they are not an enumeration of all possible histories.

The repaired execution marks all-path funding false when a provider limit
is imposed or when hard capacity is below the quota. The capacity condition
is sufficient and deliberately conservative: repeated keys may fit a smaller
store on a particular tape, but that observation is not silently substituted
for the declared eligibility condition.

| Selector, eight-query check | Advertised all-path cap | Actual total at full funding | Restricted successful limit | Restricted expectation eligible? |
|---|---:|---:|---:|---|
| Uniform | 185192 | 6476 | 11436 | No |
| Tickets | 185212 | 7006 | 11966 | No |

The restricted limits preserve intermediate provider reservation headroom.
They complete the chosen deterministic realization while remaining below
the all-path cap. The broker correctly distinguishes those facts. The
maximum public-shape check at action/state precision 32 completes with
actual total 52645 under cap 39188238 and observes peak numeric width 75
bits. Those measurements are witnesses to bounded implementation behavior,
not substitutes for the conservative argument.

## 7. Remaining obligations for the principal's combined experiment

No unresolved blocker was found in the repaired broker's reviewed boundary.
The main experiment still needs one prospectively frozen dependency closure,
separately priced procurement and reporting, trusted service linkage, and
independent post-run scoring. It must retain failed and partially purchased
episodes, distinguish all-path eligibility from a completed realization,
and propagate source-scope withdrawal into current report authority.

The inherited regret and base sampling proofs apply only while the base
path, actual positive propensities, checked selected labels, fixed random
schedule and resource premises remain intact. A changed purchase rule,
action-dependent hard admission, stale receipt, or unpriced reporter would
require a new assessment. The companion live-hard lemma review provides the
separate justification for translating both performance endpoints using
observable exact corrections.
