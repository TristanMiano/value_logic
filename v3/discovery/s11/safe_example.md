# Exact paid-evidence revision example

Codex (GPT-6), DEVELOPMENT. Continuation of [the menu construction](safe_revision.md).
The previously exhibited query-only controller has regret 9/8, but is not
optimal once randomization between querying and immediate output is allowed.

Use the implication source and costs declared there: worlds 00, 01, 11;
weights (1,1) on signs; zero flip fees; query x0 at cost 1/4; H=2. The same
operational certification rule binds every comparator, even under a point law.
The point-law optimum is (-2,-7/4,0), as checked in sr01.

Write b for the probability of immediate terminal one, c for querying, and
1-b-c for immediate terminal zero. After a negative query let u be the
conditional probability of terminal one with no flip and v the probability
of terminal one with x1 flipped. Here u+v<=1. After a positive query, terminal
zero is optimal: every permitted terminal-one revision under the remaining
one-flip cap costs >=0. Thus the three regrets, in world order, are

```math
R_{00}=2-2b+c/4-2cu,\qquad
R_{01}=7/4+c/4-2cv,\qquad
R_{11}=2b+c/4.
```

Take b=7/16, c=9/16, u=2/9 and v=7/9. Every regret is **65/64**.
All realized branches obey the two-operation cap and the conditional
constraint-preserving menu; no independently rounded mask is used.

For a lower bound, average the three regrets with weights (7/16,7/16,1/8).
Since u+v<=1, that average is at least

```math
105/64-(5/8)(b+c)\ge 65/64.
```

The maximum regret is at least this average. Consequently 65/64 is the
exact randomized minimax value over the entire admissible policy class.
The optimized class forbidden to query has value 7/4: its second-world regret
is always 7/4, and b=1/2 attains that bound. Paid evidence therefore reduces
the optimum worst-case regret by **47/112 = 41.9642857...%** in this example.
The query fee is included, but computational/source-admission costs are not.
An equally informed ordinary contingent planner optimizing the same objective
can implement the same mixture and ties. This is an explicit capability
comparison with a restricted no-query class, not evidence of superiority over
the strongest ordinary method or practical transfer.

## Changed target constraints

The menu derivation also allows a distinct target chain G with relations T_i.
Keep the original projections P_i(h) from the source F, but define permitted
flip pairs by transformed P_i(h) membership in T_i. Universal validity still
distributes over the target conjunction. The flip-count network and regret
separator are unchanged except for these history-dependent menus. A menu may
now have no complete path, even at cap m; terminal one is then unavailable.
Terminal zero remains a declared safe fallback. The old identity-always-valid
assertion in safe_revision.py is specific to target=source and must NOT be
silently reused for this extension.

Example: source F consists of all four two-bit vectors; target G is the
implication relation, excluding 10. No fixed XOR mask maps F into G, since
XOR is a bijection and |F|>|G|. Query x0; keep the original on x0=0 and flip
x0 on x0=1. This always outputs a valid target vector with at most one query
and one flip. The query enables certified repair even when no unobserved
fixed repair is admissible. This finite output-repair semantics is explicit;
it does not infer causal interventions from observational relations.

The common chain matters. For different source/target graphs, the exact
factor projections can have larger scope and the combined representation
width must be bounded. Separate low widths do not alone bound their union.

## Closest planning comparison

[Albore, Palacios and Geffner (2009), sections 2-4](https://ml.rwth-aachen.de/~hector.geffner/www.dtic.upf.edu/~hgeffner/alex-ijcai09.pdf)
explicitly represents initial logical uncertainty, sensing, knowledge of
preconditions and contingent policy trees, and compiles observations into
knowledge-level transitions. Therefore evidence-enabled feasibility is
established machinery. The candidate delta here is the specific chain-menu
factorization, costed minimax-regret comparison under a shared certification
rule, and compact private-flow adapter. The paper's contingent width and this
construction's chain width/query count are different parameters. No claim that
this adapter beats their planner has been tested.
