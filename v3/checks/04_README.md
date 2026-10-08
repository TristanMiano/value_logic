# P3-04 reconstructed finite implementation

Contributor: **ChatGPT (GPT-6 Astra Pro)**. Version `p304-reconstructed-v1`.
This replaces missing executable evidence for current closure; it is not S1 code.
[Semantics](../derivations/04_counterfactual_semantics.md) ·
[Fresh evidence](../work_logs/P3_04_2026-10-08_S2/development/README.md).

`04_counterfactual_repair.py` supplies a Python library. `Request` admits immutable
expressions, hard constraints, uniquely named soft constraints with positive
rational weights and priority tiers, known losses, and explicit scope/metadata.
`Search.advance(n)` performs up to n frontier pops. `report()` distinguishes
nonemptiness, unknown feasibility and infeasibility; optimal rank; coverage of
all optimum identities; and outer versus exact loss information. `support_report`
returns positive/negative YES, NO or UNRESOLVED separately. A fresh request needs
a fresh search. Never reinterpret an UNKNOWN result as infeasibility.

Helpers cover paired support, fixed-reference signed-Horn closure, acyclic
finite structural tables, finite function replacement with a supplied routing
mask, Boolean definitional CNF, fixed-weight integer scalarization, scalar affine
weight regions, independent rank intervals and Boolean gating constructions.
The main checker is a reproducible worked-use driver with a separate exact
point evaluator; the composition checker demonstrates a needed explicit adapter.

The finite bound is 12 Boolean coordinates, or six paired atoms, with at most
128 hard/soft rows each, eight priority tiers and 32 requested losses. Expression
inputs have at most 1,024 expanded nodes and depth 32; input rational components
are at most 128 bits. These are implementation caps, not a general restriction
on the research's value carrier. There is no general arithmetic-model oracle.

The CNF adapter accepts Boolean gates, not arbitrary arithmetic equality. The
composition checker explicitly converts the particular normality constraint
t+f=1 to XOR before invoking it. Neither native Value Logic proof acceptance
nor full arithmetic compilation follows. Known numerical gates and source rows
are mathematical constructions with their documented semantic/unit premises.

The library is for trusted, in-process use. Mutating its internal search state
or returned objects is outside its interface contract. Full request comparison
is not cryptographic authentication. Counters expose operations performed but
are not a total wall-clock, bit-complexity or memory-accounting theorem. Complete
all-source construction can be exponential; no solver-performance advantage is
claimed over the same-access ordinary constraint method.
