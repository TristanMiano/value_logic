# Transfer assumptions and limits before exposure

Contributor: **ChatGPT (GPT-6 Astra Pro)**. Stage: **PREPARATION**.
This is a source-level derivation and disjoint local-primitive check, not a
generated final population or a result for a final method configuration.

## Gate composition

The source encodes each gate by a biconditional, with a fresh positive output
coordinate. For AND, the ternary clause requires a true output when both inputs
are true; the two binary clauses require both inputs whenever the output is true.
The OR encoding is the dual. The XOR encoding excludes exactly the four triples
in which the output differs from the exclusive-or truth value. Substituting a
signed literal for an input preserves these identities. Repeated or complementary
input literals are permitted, so their induced simplifications must remain
available to ordinary methods.

The independent [local check](transfer_primitive_checks.py) evaluates all three
operators, every ordered pair drawn from two signed input coordinates, and every
assignment including the fresh output: **384 exact comparisons**. Its
[result](transfer_primitive_results.json) preserves the complete truth table and
the adapter hash. It does not call the circuit generator, draw any seed, construct
a twelve-variable final query, execute a policy, or invoke a final scorer.

At the source level, each of the two four-gate circuits uses only earlier
coordinates. For a fixed assignment to the three primary inputs, induction over
the topological gate order gives a unique extension to both circuits and the
final XOR output. The asserted miter therefore expresses disagreement of the
circuits on some primary input. There are at most nine gates times four clauses,
plus the asserted output: **37 clauses of width at most three** before any
canonical simplification. This is inside the declared 64-clause language.

The copied-circuit branch is a deliberately available structural null. A changed
gate need not change the output function: it can be irrelevant, have aliased
inputs, or be masked downstream. Independently drawn circuits can also agree.
The construction mode is consequently not a truth label. The public input omits
that mode and all gate graphs; ordinary methods receive the same CNF and can use
its visible consequences. The challenge tests composition and continuing-state
behavior inside a twelve-variable service, not new unbounded hardness or a
semantic-generalization theorem. No construction or seed is adjusted after this
review.

## Certificate representations and supplied service

The majority identity equates the disjunction of the three pairwise conjunctions
with the conjunction of the three pairwise disjunctions. Both are true exactly
when at least two of the three Boolean inputs are true. Conjoining independently
formed blocks preserves the identity. The mux construction has one active guard
for every selector assignment; its arithmetic sum agrees with the recursively
selected datum because those guards are mutually exclusive and exhaustive.
These are symbolic identities, not newly executed final-family instances.

Their difference is embedded in a signed loss using a separate coordinate. The
representation can be large even when its denotation simplifies. This is the
intended current-bound delivery comparison: representation, proof reuse,
ordinary simplification and checking compete under one installed service.
It is not evidence that the proposed method uniquely discovers the identity.
The ordinary direct receiver and shared ADD methods may erase a reuse advantage;
that remains a valid outcome. No special final-family shortcut is added after
seeing an execution.

The rank edit and nonoptimal-incumbent slot change the requested sublevel.
Checking only minimizing assignments would therefore omit part of the specified
service. The independent scalar scorer must retain every feasible assignment
whose rank is at most the supplied incumbent's rank, including all ties. The
loss shift changes the complete scope and the valid numerical bound. Supplied
incumbent and bound acquisition remain outside this delivery tariff, so a cheap
certificate does not establish a cheap action-search method.

## Paired outcomes and interpretation

Same-seed episodes supply a fixed public-population comparison, but only the
declared mathematical path fields establish a coupled ablation. A base/live
comparison preserves the base path while allowing current hardening to change
delivered forecasts or actions. Cold/reuse and mirror comparisons have their
stronger equality obligations. A mirror additionally has the same bill; path
equality alone is insufficient.

For changed stakes, two identical action sequences must have zero action effect
when both are valued under the same loss and normalization. The analyzer now
reconstructs that common objective from false-positive and false-negative
counts. Resource differences are priced at the same current normalized price.
Native acquisition decisions and retrospective repricing remain separate
catalogues. A whole-configuration mean is computed before any ordinary minimum;
per-seed switching is not a deployed ordinary control.

The report comparison likewise fixes a common reference: each paid report's own
deterministic envelope. A width is normalized by the scheduled horizon. Missing
or conflicting reports do not become successful-report-only means. The saved
development observation that the optional report supplied no width reduction
does not justify changing the basis, grid, fee, threshold, or final schedule.

These limitations are part of the prospective interpretation. No new theorem,
positive empirical finding, contribution upgrade, or final exposure is claimed.
