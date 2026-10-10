# P3-08 CNF service and ordinary-controller closure

Contributor: **ChatGPT (GPT-6 Astra Pro)**, delegated ordinary-control
implementer/reviewer, October 10, 2026 UTC. **DEVELOPMENT ONLY.**
Same-model nonblind implementation and focused reconstruction; not an
independent external review. Agent effort is unmeasured and adds **zero**
principal-clock credit. No commit, push, final freeze or final evaluation was
performed by this agent.

## 1. Implemented scope and source boundary

The parent selected the bounded-CNF proposal after the initial review. The
implemented scope is **1–12 variables, at most 64 clauses and width at most
four**. The earlier 4–16 proposal is not the implemented or frozen scope.
Empty formulas, empty clauses, duplicate literals, repeated clauses and
tautologies have explicit ordinary Boolean meanings.

The new code is:

- [p308_cnf.py](../../../experiments/p308_cnf.py): full public input, ordinary
  enumeration/DPLL services, internal checking, current exact cache, stateless
  public experts and a shape-only cost proxy.
- [p308_ordinary.py](../../../experiments/p308_ordinary.py): five ordinary
  controllers sharing the same meter, provider and output service.

No old P3-03/06/07 source was modified. The new files import the parent's
common accounting and NumericalProd bridge rather than monkey-patching an
Euler-specific receipt interface.

### API

~~~python
Query(query_id, variables, clauses,
      source_version="cnf-input-v1",
      semantics_version="bounded-cnf-sat-v1")

make_query(query_id, variables, clauses, source_version="cnf-input-v1")
service_cap(query, solver="dpll")
checked_purchase(query, limit_total=1_000_000_000, solver="dpll")
expert_predictions(query, meter)  # Six fixed binary predictions.
cost_proxy(query, meter)          # Positive public shape estimate.
ExactCache(capacity=64)

run_method(tape, method, *, seed=3081001, error_price=1, unit_price=0,
           false_positive_price=None, false_negative_price=None,
           block_size=4, action_bits=16, state_bits=16,
           unit_limit=C.MAX_UNITS, provider_limit=None, proof_cap=2048,
           fallback_action=0, cache_capacity=64, prior_cost_multiplier=1)
~~~

Query uses immutable canonical clause/literal tuples. The public supplier's
make_query sorts this input without evaluating truth; direct noncanonical
Query inputs are rejected. Canonicalization retains duplicate literals and
clauses rather than quietly simplifying the task. Full claim identity is
(semantics version, source version, variable count, full clauses); request ID
binds the delivery separately. Each receipt carries answer or None, checked
status, provider/version, full claim/request identity and an immutable common
ResourceRecord. JSON is a harness export of these bounded records.

## 2. Why the hard-answer interface is sound at this scope

The reference program enumerates all Boolean assignments, returns SAT when
one satisfies every input clause and otherwise returns UNSAT after complete
enumeration. This finite operational definition is a bounded decision-program
instance of the L_math contract. It is not a supplied compiler into the
old nat-register-v1 VM.

The DPLL producer uses unit propagation, pure-literal elimination and a fixed
first-variable branch rule. Every propagation pass either assigns at least one
previously unassigned variable, finds a terminal case or branches. Every branch
fixes another variable, giving recursion depth at most n. Duplicate identical
literals are deduplicated locally for unit detection; tautologies remain safe.
Pure-literal assignment preserves satisfiability because it cannot falsify an
unresolved clause containing that variable in the opposite polarity.

**Hard evidence does not depend on trusting DPLL's negative answer alone.**
SAT proposals are checked by an independently written complete signed-literal
evaluator on their witness. UNSAT uses either a separately checked empty-clause
or opposing-unit certificate, or a separate exhaustive Boolean-tuple checker.
The latter checks every assignment even when a DPLL defect might have skipped
a branch. A malformed producer candidate, checker disagreement or denied
budget releases no hard answer.

These are trusted local Python/checker semantics, not external certificate
authentication. The provider and controller own their receipt calls; the
cache's lower-level insertion interface assumes receipt provenance from that
trusted execution. Public dataclass fields alone do not authenticate hostile
external objects. The ordinary controller checks the receipt returned by its
own provider before retaining its label. A separately injected misbound
provider response is rejected after its actual invoice has been absorbed.

## 3. Paid operations, bounds and failure behavior

All provider operations use the common 64-bit-word tariff. Admission, canonical
order checks, literal work, DPLL temporary state, checking, acquisition, storage
and output are paid. Canonical validation uses adjacent comparisons, with
up to four literal comparisons per clause-order comparison. Independent
UNSAT tuple generation is paid before advancing its iterator.

Final output and cleanup have an explicitly prepaid envelope before truth
computation. An incomplete service returns a failure/status record and its
actual partial invoice. No failed cost is erased. The controller reserves the
requested child cap, executes that child and absorbs the actual successful or
failed invoice before interpreting the result.

Let n be variables, m clauses and L literal occurrences. The source envelope
uses at most 2^(n+1)-1 DPLL nodes and n+1 propagation passes per node. Its
per-pass bound is 24L + 24m + 128 units, including local comparisons, unit
updates and retained state. Independent complete checking is bounded by
2^n(16L + 8m + 8n + 64). An additional 4096 + 16 key_words covers admission,
fixed setup, cheap contradiction checks and prepaid final work.

These deliberately conservative public bounds remain below the one-billion
unit service cap throughout the admitted scope. At n=12, m=64 and L=256 with
default version strings, the computed DPLL envelope is **850,958,352 units**
and the enumeration envelope is **39,068,816 units**. These are reservation
bounds, not actual bills or physical-runtime claims. Actual invoices are
usually far smaller. The expert envelope is 8,192 units and covers public
input admission, both sign/purity scans and the six outputs.

The exact cache charges cold acquisition once, then charges complete key
comparisons, retained words, current receipt rebinding and FIFO eviction.
Changing source version or clause content misses even when a displayed request
ID is reused. A new request ID with identical full mathematical content and
version can reuse the paid answer. No component cache, arbitrary semantic
equivalence solver, 2-SAT solver or SAT-library optimality claim is supplied.

## 4. Ordinary methods and fairness

| Method | Actual behavior |
|---|---|
| proof_only | Bounded enumeration/checking with the supplied proof cap; an incomplete result keeps the supplied binary fallback and unresolved status |
| probability_cost | The same six public experts and NumericProd state, one uniform selected paid query per block, frozen base forecasts, greedy marginal expected-cost actions |
| exact_dpll | A cold checked DPLL call per query, including the cheap checked contradiction route |
| exact_cache | Full current cache first, then checked DPLL on a miss |
| ordinary_combo | Paid current cache; a selected label from cache or cold DPLL; optional unselected capped DPLL probes and full DPLL chosen using public shape/prior paid cost estimates and current stakes |

The probability and combined methods have access to the candidate's fixed
expert library and ordinary blocked numerical update. Their greedy actions
are not the recurrence's randomized actions. The combined method can obtain
additional labels or skip a redundant physical call using the paid cache.
Neither controller is assigned the original one-cold-purchase or randomized
terminal-action guarantee.

For the combined method, one position is selected uniformly before the block's
labels arrive. All base forecasts in the block precede label-driven updates.
Extra obtained or legitimately cached labels update the numeric state only at
the block boundary. A cached current point may improve the emitted forecast
for a later request within the block; the base forecast remains immutable,
and no new concentration theorem is claimed for that changed emitted sequence.

An optional capped probe has a prospectively fixed public cap
min(full cap, 2048 + 24 key_words). It includes the provider's checked
empty/opposing-unit shortcuts and any additional exact work that completes
within that cap. It may fail, and repeating with a full service pays both
bills. A failed probe is not treated as a cheap completed computation.

The cold cost estimate is the public shape proxy. A shape class with prior
successful full calls uses their arithmetic-mean observed cost. Failed calls
remain censored and cannot lower this completion estimate. Neither estimate is
an oracle for expected computational value. The same components remain
available to an ordinary mirror of the candidate, which the parent will
include as a separate exact translation control.

### Cheap greedy readout

The first unexecuted ordinary draft used the common generic rational envelope.
The parent correctly identified an unnecessary ordinary-method tax. That
draft is preserved in source_revisions/p308_ordinary_v1_unexecuted.py.
Before any ordinary execution, v1.1 replaced it with the direct specialization.

For q=n/d, compare

~~~text
FP_numerator * (d-n) * FN_denominator
    < FN_numerator * n * FP_denominator.
~~~

The common q denominator cancels. Only the selected expected loss needs an
unreduced rational pair. Fee and empirical-mean comparisons likewise use
bounded integer cross-products with an explicit 256-bit intermediate cap.
There is no unnecessary Fraction normalization in a policy decision.
The ordinary one-word greedy readout costs **30 units** under the shared
tariff. Exact/proof arms do not pay for an unused marginal or value-of-
computation calculation.

All method results include their configuration, immutable issued forecasts,
prospective and terminal actions, checked/unresolved status, actual invoices
and the complete meter. Physical purchase attempts and successful purchases
are separate. A globally interrupted episode retains pending, issued_trace
and rounds_issued, so scoring need not lose an already issued forecast.
The local controller setup is included. The common installed source registry
is excluded symmetrically and must be added by the parent runner.

## 5. Focused evidence and retained adverse results

The [input plan](cnf_input_plan.json) preceded service population generation.
The [ordinary plan](ordinary_input_plan.json) preceded ordinary execution.
Final source-bound focused checks are:

- [CNF service result](../development/cnf_service_final/result.json):
  512 subsets of a complete two-variable empty/unit/binary clause catalogue,
  checked with both exact services and a separate truth definition. Additional
  empty, tautological, duplicate, disconnected and maximum-shape cases pass.
  Corrupted producer proposals, budget denial at different phases, exact
  cache/version behavior and public-feature isolation are covered.
- [Ordinary result](../development/ordinary_final/result.json):
  216 dyadic/asymmetric/zero/extreme-price readouts agree with exact Fraction
  algebra. Five tiny method tapes, frozen-block readouts, selected-only
  probability feedback, censored paid probes, failed receipts, changed versions
  and misbound provider behavior pass. Full generated cohort comparison was
  **not** run by this agent.

The first service-only v1 run used the predeclared 32-query public cohort and
is retained with its exact source snapshot. It happened before the parent
requested that later full comparisons be centralized. Its 15 SAT / 17 UNSAT
split was incidental; no truth balancing was used. Its old invoices were
1,602,891 checked-DPLL units versus 4,441,169 checked-enumeration units.
These are historical v1 invoices, not current v1.1 tariff claims. Later
source-final checks deliberately skipped that cohort comparison.

One ordinary **tiny adverse repeated-query diagnostic** is retained:
both methods return the same terminal answers, and the combined controller
costs **4,794 units more than exact cache**. That is evidence against a special
learning advantage on this easy repeated service, not a global obstruction for
all CNF inputs. The source, endpoint and full cost vectors remain available to
the parent for stronger ordinary comparisons.

The v1.1 ordinary output is preserved. V1.2 adds explicit configuration fields
without changing decisions or invoices. The final checks were reissued only
to close the exact final source set after a documentation correction to the
CNF checker description. No seed, method count, label balance or selected
mathematical population was changed to obtain a favorable result.

## 6. Disposition for the parent

**Ready for the parent's common DEVELOPMENT closure and all-arm comparison.**
This is an implemented finite family and credible ordinary-control portfolio.
It does not establish that the combined controller is cost-optimal, that CNF
learning beats ordinary exact computation, or that the old recurrence theorem
already covers the greedy/optional-purchase policies. Preserve the Euler-table
obstruction alongside the new arm and report the exact candidate/ordinary
mirror equality separately from comparisons to simpler controls.

### Final source hashes

| Source | SHA-256 |
|---|---|
| v3/experiments/p308_cnf.py | 46fd3e82505b9b6af9805836a562f2f78a3436384e0b3476c4f85cec355817a2 |
| v3/experiments/p308_ordinary.py | 25ce85761c2936da3bade5f1ff995c4012f4fce5f358c2bfb5e6f05ca4690e3b |
| v3/experiments/p308_common.py | 4928a5b9c80e05b497bd93116957139252c65f393e6e12ea4c7ad4727f300a29 |
| v3/experiments/p308_broker.py | 399080c950a48c1cd935efbee8ed7769a7af54b7afa14859b5671397638e2e4d |
| CNF final result | cd4136e3b7a83c18267b880a4f412fd29563f115c355c64e7e31db8f35b979ee |
| Ordinary final result | 8349438b4dacf0ff02585d682db056f2b8b79405e6ad1c8ca738b3f97504b7e8 |
