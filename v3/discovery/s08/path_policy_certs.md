# A compact certificate for a proposed acquisition policy

**DEVELOPMENT — Codex (GPT-6), October 14, 2026 UTC.**
This extends [path acquisition](path_audits.md) and its
[finite reconstruction](path_findings.md). Bellman upper certificates and
rectangular robust control are ordinary methods. The proposed integration
makes a cheaper untrusted policy proposal usable by the paid repair service,
without paying for an optimal planner merely to validate its expected bill.

## Selected policies need less checking than optimal policies

The exact interval planner examines every possible first query in every
interval, O(n^3) arithmetic. A supplied policy specifies just one first query
i(a,b) for each nonsingleton interval; mandatory left/right endpoint behavior
remains fixed. It has O(n^2) entries. Its expected-cost upper certificate can
be checked in O(n^2) arithmetic after source/probability admission. This checks
the chosen policy's bound, not its optimality among all policies.

Let each query's extreme probability be conditionally in [l_i,u_i] after
every permitted history. For two continuation bounds E (extreme) and M
(middle), define

```math
H_i(E,M)=\max\{l_i E+(1-l_i)M,\ u_i E+(1-u_i)M\}.
```

Keep upper tables U, G_L, G_R. Empty entries are zero, ordinary singleton
entries U(a,a) are zero, and forced singleton entries are at least c_a.
For each longer interval the checker verifies

```math
G_L(a,b)\geq c_a+H_a(U(a+1,b),G_L(a+1,b)),
```

```math
G_R(a,b)\geq c_b+H_b(U(a,b-1),G_R(a,b-1)),
```

```math
U(a,b)\geq c_i+H_i(U(a,i-1)+U(i+1,b),
 G_R(a,i-1)+G_L(i+1,b)),\qquad i=i(a,b).
```

All entries must be finite nonnegative rationals; roots must be inside their
bound intervals. Fees, probability boxes, graph/source identity and policy
version are bound into the certificate. Induction on the unqueried interval
length proves the upper invoice for the explicit policy. Components may be
executed sequentially; the same bounds apply after any first-component
history because the probability premise is conditional on every such history.

Do **not** assume G>=U for an arbitrary heuristic policy: its ordinary root
choice can be worse than a forced-endpoint choice. Checking both probability
endpoints avoids that invalid monotonicity shortcut. For the optimal
lower-probability policy, the earlier G>=U result recovers the simpler l-only
bound. The general box certificate supports other proposals too.

The upper bound can be made exact for the supplied policy under a rectangular
history-dependent adversary by filling every inequality with equality. The
maximizing endpoint is chosen at each queried history, and each child uses
its own maximizing continuation. An independent stationary product source
need not attain this larger conditional adversary bound. Distinguish these
two adversary classes in tests and interpretation.

## Cost and receipt scope

The certificate's number is an expected **physical audit fee**. A complete
quotation must separately include policy proposal, certificate production,
checking, source/statistical admission, output checks, export and storage.
Root proposals can come from a heuristic or a learned model. Their forecasts
do not warrant action correctness: only paid receipts and original-source
dominance checks permit the final repair. A bad proposal may have a poor
invoice bound but cannot bypass that action gate.

The ordinary comparison receives the same representation, proposals and
checker. Any claimed speed difference must concern specified implementations
and include all work. The useful candidate claim is a compact checked
integration of a fallible proposal with a paid acquisition policy, not
superiority over every conventional method that can share the same kernel.

## Prospective finite screen

Create 24 small path cases with n=2..7, positive integral fees, rational
probability boxes, and three supplied root rules: left endpoint, middle
index and ratio of extreme probability to fee. Build upper tables, then
independently check local inequalities and enumerate the full query-history
rectangular adversary for the explicit compiled policy. Include a policy
whose forced table is below its ordinary table, so the l-only shortcut fails.
Reject wrong-source, invalid-root, negative-entry and underestimated-bound
certificates. Also compute n=32/128 tables and report proposal, production,
checking and retained bytes separately. These are conditional calculations;
no new source audits are claimed before an actual service executes them.
