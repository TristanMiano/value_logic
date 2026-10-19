# Reusing partial permission evidence across source changes

Codex (GPT-6), DEVELOPMENT. A consequence of the
[local compiler](permission_compiler.md), building on earlier proof-transport
work rather than claiming a new dynamic-reachability algorithm.

## Soundness needs an upper approximation to each projection

For a target clause on variables J, the action compiler remains sound if its
cached relation Rhat_J contains the true projection of F-and-h. Extra patterns
add extra action constraints and may hide useful edits, but cannot authorize
an unsafe one. Removing a pattern requires evidence that it is impossible.
This makes a partial, incrementally improved cache useful before all local
source questions have been resolved.

A fallible predictor may suggest which pattern exclusions are worth proving.
It must not itself remove a pattern. A checked proof of
F AND h AND (x_J=v) being unsatisfiable warrants the exclusion. A source model
with that pattern witnesses possibility; lacking a witness is not an exclusion.
The exact two-literal-source shortcut is an efficient way to supply this
evidence, not a requirement for the conservative compiler.

## Clauses change; variable meanings and receipts stay fixed

Assume each source clause has an immutable identity and proof supports list
their actual dependencies. The semantics of original bits do not change.

- Adding source clauses shrinks the possible worlds. Every old excluded-pattern
  proof remains valid, and every old projection upper bound remains sound.
  Some old possibility witnesses may fail the new clauses. Keeping their
  patterns in an upper bound only reduces available edits; exactness requires
  additional work.
- Deleting source clauses expands the possible worlds. Old possibility
  witnesses remain valid. An exclusion proof whose premises all survive
  remains valid. Restore every pattern with an invalidated proof unless a new
  proof is checked; restoration may be conservative if an alternate proof
  exists. This reintroduces the corresponding action constraints before release.
- Adding target clauses requires compiling those clauses too. Removing target
  clauses can only enlarge the allowed menu. Reuse local source projections
  for repeated variable sets; a previously unasked variable set needs evidence.

Derived forced literals have dependencies too. After a source deletion, an
old propagation path may no longer justify filtering a projection. Recompute
the closure or retain only independently checked surviving paths. Actual
queried literals persist because they were observed under unchanged meanings.
A contradiction between source and receipt is an explicit model failure, not
a reason to release an arbitrary action.

This direction avoids an unearned global-recomputation claim. A local clause
deletion can change a projection far from that clause: removing one edge in
a long implication chain may make the two endpoint values newly compatible.
Adjacency alone is not a valid invalidation rule. Actual proof support or a
sound over-approximation of its dependence is needed.

## A useful monotonicity contract

During fixed-source, fixed-target work, proving more pattern exclusions only
removes action constraints. Previously safe actions remain safe. Therefore an
anytime procedure can retain its best checked action while purchasing more
local exclusions or observations. Upon a source weakening, first restore
invalidated constraints and recheck that action. If it no longer passes, use a
currently checked fallback or abstain according to the task contract.

This improves the semantics of a partially prepared model: unresolved local
facts mean explicit lost opportunities, while checked exclusions release them.
It does not guarantee that every extra proof is economical, that the chosen
fallback exists, or that a learned proof scheduler beats conventional ones.
The complete preparation/proposal/checking bill is still the comparison duty.

The current experiment has tested exact fixed-source compilation only. This
transport protocol is derived, not yet executed. Any implementation must retain
failed checks and distinguish a conservative cache from an exact action menu.
