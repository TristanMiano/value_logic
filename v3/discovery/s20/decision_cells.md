# A decision may need less than the whole range

Codex (GPT-6), October29,2026 UTC. DEVELOPMENT; separate from V19 confirmation.

## Loss-cell signature

Fix a finite set of rational breakpoints. Partition the real line into their
singleton points and intervening open intervals, including the two unbounded
tails. Suppose each specified action's loss is constant on each cell H_j,
with loss vector v_j=(L_a(H_j))_a. This is an explicit restricted loss model.
Let J_R={j:R intersects H_j}. The worst-loss vector is exactly

    W_a=max_{j in J_R} v_ja.                                  (C1)

Thus this duty needs an attainability signature, not every endpoint of R.
For checked I subset R subset O, let J_I and J_O be their cell signatures.
Then J_I subset J_R subset J_O. With nonempty J_I, use

    l_a=max_{j in J_I} v_ja,  u_a=max_{j in J_O} v_ja.

If J_I is empty but R is assumed nonempty, min_{j in J_O} v_ja is a valid
lower bound for each action. Empty O signals inconsistent premises instead
of an optimal action. This does not certify R nonempty when I is empty.

For minimax regret replace v_ja by

    g_ja=v_ja-min_b v_jb

before computing all bounds and reductions. An attainable bad cell supplies
a lower bound even without a complete reconstruction of the remaining range.

## Sharper stopping certificate

For any proposed action a and at least two actions, put

    eta_a=max(0,u_a-min_{b != a} l_b).                         (C2)

With one action put eta_a=0. Then W_a-min_b W_b<=eta_a.
Indeed W_a-min_b W_b=max(0,max_{b!=a}(W_a-W_b)); replace each difference
by its upper bound u_a-l_b. This improves the earlier bound by not charging
uncertainty about a's own worst loss as a possible gain from choosing a again.
If eta_a=0, the chosen action is minimax optimal even when its exact worst
loss remains unknown. The fixed-model computation stopping argument from
partial_decisions.md applies with eta_a as well.

One can select an action minimizing u_a as a conservative default, or minimize
eta_a for the smallest certified suboptimality gap. These objectives differ;
neither is declared universally correct. The intended decision criterion,
action set (including any allowed randomization), costs and stopping tolerance
must be stated by the caller.

## Irrelevant unresolved cells

If J_I is nonempty, an unresolved cell j in J_O minus J_I is irrelevant to
the **entire worst-loss vector** whenever v_ja<=l_a for every action a.
Adding or removing j cannot exceed an already witnessed maximum. Conversely,
if some v_ja>l_a, the support J_I union{j} increases that coordinate, so this
test is necessary for irrelevance across all intermediate supports permitted
by the bracket alone. It need not be necessary after using further source
constraints, and a cell relevant to the vector may still be irrelevant to
the identity of an optimal action.

Do this comparison on regret vectors when minimizing regret. For instance,
two cells with loss vectors(100,101) and(101,101) have regret vectors(0,1)
and(0,0). A witnessed second cell makes the first irrelevant to maximum
loss but not to maximum regret. Applying loss dominance to a regret duty
would silently change the question.

## Endpoints are part of the contract

Closed-band intersection is insufficient for open loss cells. A range
consisting only of0 intersects[0,1] but not(0,1). For an interval[a,b] and
open cell(l,u), intersect the bounds. If the resulting endpoints differ,
their rational midpoint is a witness. If they agree at q, it is a witness
only if l<q<u, omitting missing infinite endpoints. Singleton loss cells
are tested by ordinary point containment. This handles degenerate ranges,
touching boundaries and unbounded tail cells without floating approximation.

These constructions are elementary task-specific robust optimization and
abstraction. They are not new generic decision theory. The useful development
question is whether the exact receipt service can expose this smaller query
contract without confusing possibility, actuality, loss and regret. The
fixed contribution event remains unchanged; standalone novelty UNASSESSED.
