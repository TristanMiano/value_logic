# Receipt-mask specialization: accepted with a preserved syntax repair

Codex (GPT-6), October29,2026 UTC. P3-11-A1 same-model reconstruction.

[Mask.lean](Mask.lean) embeds the unchanged accepted Layer and Count units.
It defines finite Boolean masks, enumerates all available submasks of the
remaining state, removes the chosen submask, and accepts only an empty
terminal state. `paths_iff_good` proves equivalence with the explicit legal
layer partition predicate. `good_assigns_once` and `all_receipts_once` prove
pointwise exact coverage, with no duplicate receipt assignments. The selected
path is legal and dominates every legal alternative; absence means no legal
partition. This closes the planned finite-mask connection left open in Layer.

The first retained compiler attempt failed because a proof binder used the
reserved Lean keyword `local`. a02 renames it `availableT` and passes in
946,162,100ns. Both source versions and compiler outputs are retained. The
precompiler source assembly also initially failed under Windows' default
cp1252 decoding; explicit UTF-8 fixed that before any compiler exposure.
Neither failure indicates a mathematical counterexample or hardware problem.

Accepted source SHA256:
`75bb36919168c4a8f7496836124af6131c454d0f0d367e296518e0b30ae7de5a`.
The accepted printed theorems use only standard Lean axioms; no proof hole,
new axiom or unsafe declaration is present. Compiler time was excluded.

The enumerated mathematical recurrence is an exact specification. It does
not verify Python's bitwise representation, memoization implementation,
dictionary complexity, serialization, or a hardware execution chain. Its
exhaustive-choice semantics plus the earlier written table argument justify
the memoized algorithm; the Count unit and resource review carry the cost
bound separately. No new novelty credit follows from this optional proof work.
