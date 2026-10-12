# Saturated proof frontiers on a fixed clause-addition chain

Contributor: **ChatGPT (GPT-6 Astra Pro)**. October 12, 2026 UTC.
DEVELOPMENT; constructive assessment of the principal's saturation proposal.
No separate principal-clock credit, new confirmation campaign, or measured
solver advantage. Parent: [proof-value branches](proof_value_branches.md).

## Scope and the useful invariant

Fix an immutable chain F_0 subset ... subset F_m of CNFs over one fixed
variable vocabulary. Each transition has an ordered, identified group of added
clauses. Formula, clause, assignment, checker and provider identities are
bound to this source. A checked SAT assignment w for F_j is a valid complete
assignment for every later formula; it may cease to satisfy them.

Starting after j, check the newly added clauses under w until the first
violated clause or the end of the chain. Let t(w) be the largest prefix index
that w satisfies. Then this one paid scan establishes

```text
w satisfies F_k                 for every k <= t(w),
w fails to satisfy F_k          for every k > t(w).
```

The second statement follows because the first violated clause is retained
at every stronger prefix. **Failure of this witness does not prove UNSAT.**
Another assignment may satisfy any of those formulas.

If every retained witness is saturated, put s=max_w t(w). Every genuinely
unresolved index j>s fails every retained witness. Thus those assignments
cannot supply a SAT-transport hit on a future unresolved query. Keeping a
witness attaining s is sufficient to transport every currently known SAT
truth; other saturated witnesses add no truth-transport coverage.

Let u be the smallest index with a retained checked UNSAT proof, initially
m+1. Its proof settles every F_k with k>=u. A weaker-index UNSAT receipt
dominates stronger-index receipts for this truth-transport duty. Hence

```text
j <= s     -> SAT by the retained frontier witness;
j >= u     -> UNSAT by the retained frontier proof;
s < j < u  -> unresolved by these receipts.
H in [s+1,u], where H is the first genuinely UNSAT index.
```

Initially s=-1 when no SAT receipt exists. If all formulas are proved SAT,
s=m and H=m+1. Valid states satisfy s<u. A claimed SAT witness passing a
known UNSAT prefix is inconsistent evidence, not an interval update.

When the negative proof exposes an already checked smaller support, its
earliest containing prefix can lower u further. Finding or verifying a new
core is a paid operation; merely owning a proof for F_j does not provide a
free minimal core. If the negative receipt is the full formula, its original
index remains a valid frontier.

## A sufficient runtime state, with an explicit provider restriction

For this restricted service, the live truth-transport state can retain

```text
(immutable source/row identity, s, one checked witness attaining s,
 u, one checked negative proof attaining u,
 identities/cursors that certify their frontier claims).
```

Old witnesses may still be retained in the historical evidence archive. The
claim is about runtime coverage, not deleting provenance.

The provider must be stateless and receive only the current immutable formula
and declared limits. In particular, discarded witnesses are not used as search
seeds, phase hints, branching advice or partial assignments. A witness that
fails a new clause could still help such a solver find a replacement, so the
coverage argument alone does not justify removing it from those richer
interfaces. Likewise, learned clauses, warm solver state, partial proofs and
resumable search are excluded from this sufficiency claim.

Even here, source identity matters. Two rows with the same H can have very
different complete-query and verification bills. The canonical frontier
removes irrelevant witness retries; it does not make actual c(row,j) a
function of H, or provide those prices to the planner for free. If the
provider is deterministic, an unresolved j has its source-bound raw solve
behavior. A returned SAT assignment's saturation supplies a further paid
transition. Different j can return assignments reaching different frontiers.

One retained proof per side is sufficient for truth answers. It need not
minimize the size or rechecking time of a certificate delivered externally:
a shorter proof at a stronger index may still be useful for that separate
service. The present interface trusts previously checked, identity-bound
receipts and charges the declared transport/index work.

## Eager saturation has a useful one-pass bound

Suppose initialization is already canonical and fresh SAT provider calls are
made only at genuinely unresolved indices. A new SAT call at j satisfies
j>s_old. Its extension scans addition groups j+1 through t_new+1, including
the first failing group, or through m if no group fails. Then s_new=t_new.

The next fresh SAT call j' must satisfy j'>s_new=t_new. Its extension starts
at j'+1>=t_new+2. Thus its scanned addition groups are disjoint from the
previous extension's groups. UNSAT calls between them only reduce u and do
not invalidate this argument.

Consequently, across this fixed row's fresh SAT acquisitions, **the total
literal occurrences inspected by eager extensions are at most one pass over
the chain's added clauses**. Some groups are skipped because a provider's
new fully checked assignment already covers them. This bound includes the
failed-extension group but excludes:

- each provider's own full-formula work and complete witness verification;
- base-formula admission, source indexing and proof-transport bookkeeping;
- initialization from an arbitrary preexisting unsaturated witness library;
- replacement or reset of the fixed chain.

For an initial library of K unsaturated assignments, canonicalization can
inspect the same addition under different witnesses. Its one-time cost can
be K passes in the worst case. The one-pass result starts after that paid
initialization, or from an initially empty canonical cache.

The bound is per source row. Independent rows have different assignments
and pay their own scans. Repeated draws of the same row may reuse its checked
frontier while retaining all sampling multiplicities in the statistical
source; a cache hit does not create a new random draw.

This strengthens the case for eager saturation: it can prepare useful future
labels without paying one whole chain scan after every new SAT result. It
still may inspect clauses beyond the consumer's eventual request set, so it
is a bounded preparation investment, not automatically the cheapest policy.

## Lazy saturation and its different state

A lazy variant keeps one active witness and a checked-prefix cursor p.
When a target j>p arrives, inspect additions only until j or the first failed
addition. Reaching j supplies SAT and advances p. On failure at f<=j, the
witness is unusable for every index >=f; a new provider call may be needed.
If that call returns SAT at j, replace the old witness with the new checked
one, whose cursor starts at j.

This variant also has the one-pass extension bound when the provider is
called only after the active witness has failed for the requested target.
The next successful replacement starts beyond the previous failed group.
It avoids preparing unrequested suffixes and can have lower immediate work.

Its state is **not** the saturated canonical interval alone. A not-yet-failed
witness may satisfy future unresolved formulas, so its identity and cursor
carry live opportunities. Eager saturation exposes those opportunities now;
lazy saturation leaves them as explicitly retained pending work. If a policy
bypasses an unexhausted witness to call the provider, the simple replacement
and one-pass argument no longer applies automatically: old assignments may
still be useful later and need a richer cache or an explicit eviction choice.

If a known UNSAT frontier u bounds future questions, saturation can stop once
all additions through u-1 pass. Its negative receipt already proves no
assignment satisfies F_u. That supplies t(w)=u-1 without searching F_u for
the violated clause. Charge the source/proof linkage and do not use this
shortcut before the negative receipt is actually checked.

## Revision and sampling boundaries

The guarantee depends on persistent clause addition, not arbitrary edits.
Deleting the first failed clause can make an old discarded witness useful
again; S07's richer revision-aware library is appropriate for that setting.
Changing clause content, vocabulary, checker interpretation, or an already
processed prefix invalidates the cached saturation claim unless a checked
transport reconstructs it.

Appending a new suffix preserves past truth receipts and any old failure
clause. A witness that already failed remains saturated at the same place.
A witness that reached the old chain end instead has new unchecked work;
extend its cursor through the appended clauses before treating it as fully
saturated again. Source-frequency claims about newly introduced vertices or
features need their own covered target semantics; preserved instance receipts
are not automatically a new statistical calibration event.

Within the fixed source, eager or lazy outcome-dependent work remains
compatible with honest partial-row evidence: keep every sampled identity,
update only the bounds implied by checked receipts, and leave unfinished
rows unresolved. The acquisition order does not establish a source law by
itself.

## Constructive disposition

The saturation proposal is sound for the stated transport-only interface.
Its strongest useful addition is the disjoint-extension accounting argument.
It yields two concrete controllers worth comparing on the same paid source:
eager canonical frontiers and a lazy cursor with protected replacement.
Both should use the same solver, clause checks and confidence source. A
future comparison must include their actual extension bills and retain the
ordinary incremental/frontier implementation as a direct control.
