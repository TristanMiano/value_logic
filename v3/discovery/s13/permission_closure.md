# Forget model claims while preserving exactly the allowed actions

Codex (GPT-6), DEVELOPMENT, October20,2026. A new adapter within the existing
permission/source family. Ordinary Galois closure and weakest-precondition
constructions are direct antecedents; the closure identity itself is elementary.

## The weakest fixed-task warrant

Let X be a finite world space, A0 a fixed available action set, and G_a the
worlds in which action a meets the declared goal. For nonempty source F define

```math
A(F)=\{a\in A_0:F\subseteq G_a\},\qquad
W(F)=\bigcap_{a\in A(F)}G_a.
```

An empty intersection is X. Then F is contained in W(F), and A(W(F))=A(F).
One inclusion follows because every previously permitted action was included
in the intersection; the other follows from F being a subset. Moreover W(F)
is the largest source preserving those permissions: any such source must be
inside every G_a for a in A(F). Thus a supplied event that the actual world
belongs to W(F) is sufficient for every initially permitted action, even when
many other predictions made by F are false. If A(F) is empty, this deliberately
vacuous warrant supplies no initially permitted action.

This retains fewer claims than preserving all task-coordinate projections.
It is specific to the goal, action set and action semantics. A changed goal or
action menu does not inherit the same permission-equivalence statement.

## A two-pass binary compiler

Take Boolean worlds and coordinate toggles: action a sends x to x XOR a.
Let the common post-action goal G be a 2CNF relation. Define the unrestricted
operator P(S)={a: every x in S has x XOR a in G}. Each goal clause involves
at most two coordinates. Enumerating the corresponding projection of S and
forbidding the shifted clause-falsifying masks compiles P(S) as 2CNF.

If A0 is itself given by 2CNF, first compile A=A0 AND P(F), then compile
W=P(A). Symmetry of XOR makes this second formula exactly W(F). This is the
same ordinary permission compiler run twice, with worlds and masks exchanging
roles. Its output is binary even when F is a union of many binary models.
For a union of M 2CNF models, each initial width-two projection can be obtained
with at most four M ordinary satisfiability queries. The second pass projects
the binary A. Charge these queries, clause generation, canonicalization and
storage; there is no claim that the setup is free or that a full-world model
description was learned from nothing.

For g goal clauses, the raw first-pass count is at most4gM satisfiability
queries and the second at most4g; unary clauses require fewer. This count is
only a simple upper bound, not a full computation bill or a measured advantage.
Once W is compiled, truthful unit receipts can condition W using the binary
service. The original coverage event continues to warrant this weaker source.

Let K2(F) denote the strongest binary relation containing F. Every shifted
goal is binary, so K2(F) is contained in W(F). The containment can be strict.
For three bits x,y,z let G forbid x=y=1 and y=z=1, and
F={000,010,100}. Only the identity toggle is permitted. W(F)=G contains five
worlds, while K2(F) still requires z=0 and contains only the three F worlds.
Actual world001 is outside the complete model and its binary hull, yet all
initial permissions remain valid. The example is a semantic separation, not
an empirical saving or an interesting action-selection benchmark by itself.

## New observations buy soundness, not conditional equivalence for free

For a later truthful receipt h, F AND h is contained in W AND h. Therefore
every permission proved from W AND h is valid under the original W warrant;
it may omit permissions that the more restrictive F AND h would suggest.
The equality A(W)=A(F) at entry does not imply equality after arbitrary h.
Compiling W afresh from F AND h would require a new conditional adequacy
premise; the old event x in W(F) does not license that strengthening.

This distinguishes two useful products: the earlier Q-plus-petal envelope
preserves a prescribed conditional projection service, while this closure
preserves a fixed action menu and goal with a weaker initial premise and a
binary representation. Neither is universally preferable. If every binary
goal is allowed to change later, retaining all width-two projections is the
natural stronger interface again.

## Learning boundary

On fresh deployment cases one can audit membership in W instead of membership
in F. This can admit a model that is globally false while its fixed action
permissions remain reliable. Any statistical guarantee still needs the paid
observations required to check W, the correct population assumptions and
selection control. The earlier binomial/Learn-then-Test construction applies;
this algebra supplies a different property to test, not a new statistical law.

## Cheap development screen and limitations

closure_probe.py passed542 nonempty finite panels generated from1439 binary
models, with3942 receipt checks and385 explicit witnesses outside the proposed
maximal closure. It found317 strict relaxations of the full binary hull and
101 strict losses of conditional permissions. Source/output hashes bind the
executed screen. Total harness time0.1765885 seconds is not an arm comparison.
These are exposed finite checks by the same model, not independent validation.

The simplest generated conditional counterexample has goal x XOR y=1 and
source{(0,1),(1,1)}. Initially no toggle works on both worlds, so W is the
whole square. After observing x=0, the original source suggests identity or
flipping both coordinates; the retained square still permits neither. This
checks the stated limitation, including its vacuous-initial-menu boundary.

Binary satisfiability supplies *a feasible* action, not a cheapest weighted
action. Minimum-cost satisfaction of arbitrary positive binary clauses
already contains minimum vertex cover. Any later optimization service must
pay for its solver or state a tractable restriction.
