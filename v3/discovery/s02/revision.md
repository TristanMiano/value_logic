# S07: explicit edits with local evidence maintenance

Codex (GPT-6), October 11, 2026. DEVELOPMENT. New branch within C001,
descending from S01/S04 and the inherited versioned-source contract.

## 1. Why change the input representation

The previous CNF broker matched complete immutable keys and charged full
admission/revalidation. Those charges defeated earlier reuse economics.
Counterfactual requests frequently arrive as *edits to a specified formula*.
A different concrete input contract can preserve checked structure by
construction and charge validation of the actual edit. This is not permission
to treat a changed arbitrary input as equal to the old one.

Represent the active formula by an immutable base and a locally validated
sequence of add/delete operations on stable clause IDs. The vocabulary,
variable count, literal semantics and provider version stay fixed. Every edit
names the expected parent version. Reject a wrong parent, reuse of a live ID,
deletion of a missing ID, or a malformed/out-of-range literal. External mutable
objects must be copied/admitted before they enter this contract. Historical
objects remain immutable. A namespace/version change falls back to fresh
admission; it is not a cheap clause edit.

The service answers ordinary SAT for each resulting finite formula. It does
not assign semantics to an impossible antecedent, select a repair distribution,
or identify a causal mechanism from observational data. Its counterfactual
operation is an explicit syntactic replacement under fixed interpretation.

## 2. SAT witness transport

For a retained complete assignment w, let v_w be the number of active clauses
it violates. Store each active clause's satisfaction bit under w. Adding a
clause evaluates only that clause and increases v_w if false; deletion looks
up the stored bit and decrements v_w if necessary. Inductively v_w equals the
current number of violated clauses. Hence v_w=0 warrants SAT after any valid
edit, even after earlier edits invalidated that witness and later repaired it.

For K retained witnesses and delta edited literal occurrences, maintenance
takes O(K*delta) bounded-word work plus edit admission and index operations;
storage is O(K*m+n*K) in the simple satisfaction-table representation. Full
initial evaluation and insertion are charged. Keeping K small is an operational
choice, not a free unbounded model library. Merely retaining one witness may
miss other satisfiable regions; failure to find a surviving witness means
unknown, never UNSAT.

This can be demand driven: check only a selected witness on a new clause and
keep per-witness edit cursors, paying all intervening edits when it is next
requested. A fallible selector can choose useful witnesses, but correctness
depends only on the completed replay. Eager and lazy variants trade storage,
background maintenance and latency; both need full prices.

## 3. UNSAT support transport

A checked UNSAT subformula U remains UNSAT in every active formula containing
all clauses of U. Retain its exact clause IDs/content and a count of support
clauses currently absent. Update this count from validated edits. Zero absent
supports warrants UNSAT; deleting a support suspends the warrant and restoring
the identical clause can reactivate it. A new clause under a reused ID cannot
masquerade as the old support. Either IDs are never recycled or identity must
include immutable content/version.

Using the entire previously checked UNSAT formula as U needs no free core
extraction, but may lose reuse on deletions. A smaller core must be discovered
and verified at its actual cost. Multiple cores can offer a coverage/maintenance
tradeoff. A resolution proof or exhaustive finite verifier can establish U;
an incomplete solver failure cannot. This is ordinary monotone proof reuse.

## 4. Expected benefit and the comparison that matters

This is a candidate for a useful *integration*, not a claim that incremental
SAT, witness caching, dependency tracking or truth maintenance are new.
Compare fresh shared solving, complete-formula witness rechecking, ordinary
incremental SAT under assumptions, and the identical edit-aware kernel. An
ordinary implementation receives all edits and can use the same transport.
The target is a supported resource consequence of the source/evidence interface,
not strict superiority over a class containing itself.

On a sequence whose edits preserve a retained witness, total clause evaluation
work is one initial full check plus evaluations of added clauses, rather than
one full check per version. This conditional consequence is clear, but no
material-positive claim follows until full setup, indexing, retention, solving,
failed witness trials and honest distribution/sequence scope are accounted for.
An already incremental ordinary solver may be equally cheap or cheaper.

## 5. Prospective developmental probe

Implement a bounded local service with explicit immutable clause identities,
version validation, paid witness/support maintenance, and the repository's
existing exact CNF solver as a shared fallback. Start with short add/delete
streams generated without solving to choose favorable outputs. Include
preserving edits, witness-breaking edits, true semantic changes requiring
fallback, and wrong-parent/recycled-ID rejections. Report operation categories
and wall time separately. Full-formula witness rechecking and the identical
delta kernel are mandatory controls. If this merely demonstrates an elementary
incremental shortcut, retain that limited result and develop a harder use case.

### Probe refinement before execution

Use native MiniSat22 through `python-sat==1.9.dev15` for **all** fallback calls,
including the ordinary incremental-assumption control. This is a stronger and
more relevant solver control than the older bounded DPLL prototype. The new
probe trusts that local native solver for UNSAT; SAT models are independently
clause-checked. Thus this probe does not inherit the older provider's independent
UNSAT-verification contract. It is a separate developmental service, with that
trust limitation explicit. Dependencies were installed outside the checkout;
installation time is O, excluded from research.

Measure warm stream execution including state creation, all edits, validation,
failed reuse, solver calls and cleanup; record common dependency/import setup
as excluded, and do not call this a cold complete-cost benchmark. Diagnostic
operation counts are not primitive tariffs. Keep the implementation/control
shared: the `native_delta` integration is also the identical ordinary kernel.
The stream is generated before solver calls, with no outcome-based filtering.
It includes explicitly declared tautological edits as easy structural controls.
Clauses are registered once; `off`/`on` disable/restore the same immutable ID.

## 6. A lazy library with one blocking clause per witness

Eager K-witness maintenance costs work on all K witnesses at every edit, even
if the first witness still answers the request. A simpler lazy construction
keeps an activation log A: append the clause ID on each `add` or `on`; an `off`
only changes active membership. Each witness w keeps a cursor into A. Its
assignment never changes. A cursor at the end certifies that w satisfies all
currently active clauses, provided it began from an independently checked
snapshot or from the start of the log.

When w is requested, scan from its cursor. An inactive clause is skipped; a
satisfied active clause is checked and skipped. Stop at the first active
violated clause, leaving the cursor on that entry. This clause remains a cheap
reason to reject w while present. If a later request disables it, resume past
it and check the intervening activations. Re-enabling a previously skipped
clause appends a new entry, so a reactivated violation cannot be missed.

Invariant: every active clause either has a last activation at or after the
cursor, or was proved satisfied under w. Initially this follows from the paid
full witness check. Each cursor step preserves it; inactive-to-active changes
append evidence obligations. Reaching the log end therefore establishes SAT.
Failure only rejects this assignment, not the formula. No literal truth needs
to be guessed. The trigger/cursor mechanism is an ordinary dependency-tracking
idea, not a claim of novelty over watched clauses or incremental computation.

For a fixed retained witness, each activation entry is passed at most once
between resets. Total cursor advances are at most K*|A|, plus one failed test
per attempted blocked-witness request. With clause width d, the corresponding
literal-work bound is O(d*(K*|A|+attempts)), excluding full witness admission,
solver fallback and data-structure costs. Eager updates have O(K*delta) work;
lazy requests may save most of that work when one current witness stays useful,
but can instead incur long catch-up latency. No universal strict improvement.

Use a small bounded LRU library initially. A new fallback witness enters only
after full checking; set its cursor to the current end. Eviction forgets that
witness, not its historical evidence record. This is a retention heuristic,
not an optimal or learned policy theorem. Test capacities 1,2,4,8, and preserve
failure cases where the extra memory or scans fail to repay their cost.

An unbounded activation log is not a production memory policy. With a known
active-clause cap M and K<=M, rebasing after 2M activations replaces the log by
the current active IDs (<=M) and resets all cursors; this costs O(M+K) index work
and may cause O(K*M*d) rechecks. At least M subsequent activations occur before
the next such rebase, so those rechecks add O(K*d) amortized work per activation.
The log is then O(M), while a blocked witness can still be checked locally.
This conditional bound requires the explicit fixed cap and charged rebases.
