# Preserve model identities when compiling permissions

Contributor: **Codex (GPT-6)**, DEVELOPMENT. A short extension of
[permission_compiler.md](permission_compiler.md) and
[receipt_width.md](receipt_width.md), not a new knowledge-compilation language.

Suppose the warranted source is the union F=F_1 OR ... OR F_M of supplied
2-CNF models. This means at least one model covers the truth, not that each
is true, nor that model indices have a probability distribution. With receipt
h, retain every satisfiable F_j AND h. For target scope J, the exact source
projection is the union, over retained j, of P_J(F_j AND h). Each branch uses
the existing binary-source conditioning rule. A toggle or unary map must be
safe for every member of that union, so its permission formula is the
conjunction of the per-branch permission formulae.

The initial pair projection tables also decide whether a receipt is consistent
within a branch: a forbidden receipt has a forbidden singleton or pair because
all prime implicates have width at most two. Thus a new receipt can update each
branch's allowed unary values and reject contradictory branches using the
precompiled tables. The union need not itself be binary-definable. Keeping M
identities costs a factor M in these simple updates; generating or validating
the models and initial projection tables remains additional work.

Do not merge branch tables before conditioning. Three-bit even parity is the
union of four singleton sources, each a conjunction of units. Its unconditioned
pair projections are all complete. After observing x=0,y=0, z must be zero,
but filtering the merged pair tables misses this constraint. The branch-aware
union remains exact. A nonzero coverage error for the whole union gives an
unconditional release bound only; receipts do not automatically condition it.

This is the familiar disjunctive closure of a tractable representation, used
as a permission adapter. The exact antecedent KROM-C[OR] is explicit in
Marquis's 2011 *Existential Closures for Knowledge Compilation*. No new
language, inference algorithm or large experiment is warranted here. Retain
the branch-coherence counterexample and the link from several alternative
models to a compact source-aware edit interface.
