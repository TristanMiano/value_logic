# Why broad random audits do not cheaply validate narrow clauses

Codex (GPT-6), October 19, 2026. DEVELOPMENT early connection screen, Q1–4.
Combines the fixed-population audit and permission branches; no new harness.

Let a fixed predicted vector xhat name N meaningful Boolean claims. Uniformly
audit m distinct coordinates and continue only if all match. For a proposed
coordinatewise unary map a and CNF postcondition G, consider the number of
prediction errors needed to falsify G after a. There is no other source promise
in this screen. Repeated or tautological literals are first simplified.

For one clause, a coordinate overwritten to satisfy its literal protects that
clause for every original truth vector. An audited unchanged/negated coordinate
whose known output satisfies the clause likewise protects it. Discard those
protected clauses. For an unprotected clause, every remaining nonconstant
coordinate map is identity or negation; its literal is falsified by exactly one
original bit value. The minimum number of unobserved prediction errors needed
to falsify it is exactly the number k_C of its literals true at a(xhat).
Audited false literals cost no errors and unobserved predicted-false literals
remain false. Distinct coordinates make this pattern attainable.

Thus a nontrivial CNF's minimum error distance to failure is min_C k_C, at most
its clause width. If all clauses are protected there is an exact release
certificate already; if some k_C=0, the predicted vector itself violates the
target. The useful intermediate case for binary targets has k in {1,2}.

The general all-pass population rule requires

    choose(N-k,m)/choose(N,m) <= alpha.

For k=1 its left side is (N-m)/N, requiring m>=ceil(N*(1-alpha)). For k=2
it is (N-m)*(N-m-1)/(N*(N-1)), requiring approximately
m >= N*(1-sqrt(alpha)). At alpha=0.01 these are about 99% and 90% of the
population. This explains why a broad cardinality audit is generally a poor
way to justify low-width source/target constraints. It is not a lower bound on
a task-directed verifier: checking a small relevant support may be much cheaper,
and safe overwrites can remove the uncertainty altogether.

Large-margin targets, such as a majority statement far from its threshold,
can have k proportional to N and admit a short population audit. That positive
case is retained in premise_audits.md. The contrast is structural, not evidence
that random audits are broadly superior or inferior. Weighted selection,
logical restrictions on possible error patterns and new actual receipts can
change the margin, but the cost of obtaining those restrictions must be paid.

**Disposition:** do not build a uniform-audit source-admission benchmark for
binary safe-edit tasks merely to combine two available mechanisms. Their
elementary error margins are unfavorable. Prefer checked task-specific source
facts, direct support verification, or a naturally robust aggregate task.
