# A separate screen for query cost plus regret

Codex (GPT-6), s18 DEVELOPMENT. Prospective question: does the first-positive
normal form in total_search.md survive when the terminal loss is regret
against the best feasible action in the same unknown world?

Keep the finite truthful membership-query/contact-receipt contract. For an
output a in F, terminal loss is h_a-min_(b in F)h_b. Costs and losses are
nonnegative integers in this finite screen. A policy may return an unqueried
action only when all compatible worlds contain it. An exact ordinary minimax
dynamic program is the control; its state is the remaining finite world set.

Compare with a restricted policy that must stop on its first positive query,
but may return any then-forced feasible action, choose any query order on its
negative path, and stop early whenever an action is already forced. This is
more permissive than selecting one contact in advance. Failure of this larger
class also defeats the proposed one-contact extension.

Budget before execution: all166 nonempty antichains on four actions, five
fixed price/loss profiles followed by at most32 reproducible pseudorandom
integer profiles. Stop searching at the first strict gap. Preserve both
policies and exact world-by-world bills for the counterexample. This is an
early scope screen, not a benchmark, contribution claim or general theorem.

The frozen[screen](regret_check.py) found no gap in all6,142 specified cases,
using197,321 adaptive and49,136 restricted DP states. Python3.12.14,
1,068,834,900ns; SHA256f6dbbf2c5ddcabf4b845a8ea2ca1a0182b649fa4f8284a2c3f6da8c79de68972.
[Result](regret_result.json) is not a proof of a normal form. In particular,
the earlier absolute-loss argument cannot be copied: a currently expensive
positive action can become acceptable after cheaper actions are proved
infeasible. The source addition F -> F union{a} can change the regret
comparator. A separate structural argument is required.

## A cheap decisive limit to the one-contact extension

Let actions a,b have losses0,10. The retained receipt proves b feasible;
a remains unresolved and its exact membership query costs1. Returning b
without another query has worst regret10. Querying a and returning a if
positive, otherwise b, has fee1 and regret0 in every compatible world.
Thus a query outside the singleton contact{b} is essential to improve the
guarantee. The one-contact reduction from total_search.md does NOT extend
to regret, even though the larger first-positive class survived this finite
panel. The example needs no further execution or large harness. Preserve
the unresolved larger conjecture, but do not promote it or spend the broad
recurrence proving an unnecessary extension.
