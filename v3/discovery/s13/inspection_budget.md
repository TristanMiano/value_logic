# Tune reliance through a hard inspection budget

Codex (GPT-6), DEVELOPMENT, October21,2026. Adapter of inspect_or_edit.md,
not a new candidate family. Standard prediction-assisted algorithms are the
comparison framework. Two different denominators below must stay visible.

Let B be the cheapest blind write certificate for the implication goal and
let C_pred be the cheapest confirming certificate at the predicted Boolean
world: a matching sign costs min(query fee,write fee), a nonmatching sign
costs its write fee. Neither benchmark uses unverified predictions as facts.
Assume the goal is feasible, all costs are nonnegative, observations are exact,
the original world is stable until commit, and writes have the declared effects.

For any 0<lambda<=1, replace each query price q_i by q_i/lambda when choosing
the fixed certificate. Keep actual write prices. A matching selected sign is
implemented by inspection if that option wins; other selected signs are written.
Let Q,W denote the actual query and planned-write totals. The ordinary cut
optimizer's scaled objective satisfies

    Q/lambda + W <= B,

because the blind certificate remains an allowed competitor. Hence Q<=lambda*B.
Buy all chosen queries, then recompute the cheapest safe completion R*(h).
The blind certificate is still available, so the executed fee satisfies

    C(x)=Q+R*(h) <= (1+lambda)*B

for EVERY world x, independently of prediction accuracy. If all queried
predictions match, the original plan remains feasible and

    C(x) <= Q+W <= C_pred/lambda.

For the last step, evaluate the scaled optimizer on a C_pred-optimal plan:
Q_pred/lambda+W_pred <= (Q_pred+W_pred)/lambda. Reoptimization can only help.
Thus the endpoints interpolate between the earlier2B guarantee at lambda1
and an arbitrarily small relative overspend against blind writing. At lambda0,
use blind writing directly; division by zero is not part of the algorithm.

An error-sensitive statement also follows without any stochastic assumption.
Let R_miss be the cost of writing only the selected signs whose queried
predictions were wrong. Then

    C(x) <= min(C_pred/lambda + R_miss, (1+lambda)*B).

This selected, write-weighted error differs from an unweighted count of wrong
predictions. The guarantee controls purchases, while feasibility follows from
receipts and writes. Cut computation, prediction acquisition, locking and
transaction overhead remain separate charged resources.

## A one-bit lower bound prevents inflated claims

Consider one unknown bit, goal final1, write fee1, predicted bit1, and query
fee q in(lambda,1). Any deterministic policy with all-world hard fee at most
1+lambda cannot inspect: the world0 would then require fee q+1>1+lambda.
It must write at fee1 even when the prediction is correct. But C_pred=q.
Letting q decrease to lambda shows that no uniform factor below1/lambda
against C_pred is possible under this hard blind-relative budget, even in
the one-bit subclass. The scaled-query algorithm meets that lower-bound
tradeoff. This is not a lower bound for expected-budget randomized policies,
and not competitiveness against the fully adaptive stochastic optimum.

The repeated ordinary implementation ties. The useful synthesis, if any,
is the exact query/write certificate interface and its explicit reliance
parameter. Existing explorable-uncertainty work already combines untrusted
predictions, certificates, minimum covers and robust fallbacks. Those papers
use stronger optimal-query benchmarks for their own tasks; their numerical
ratios cannot be compared to this blind-write ratio as though the duties
were equal. A natural configuration workload and complete controller costs
are still needed to establish practical gain.

The first budget_probe.py execution passed45 finite rational panels,
225 scaled-cut plans and2790 plan/world executions. Independent certificate
enumeration checked the recourse and both fee bounds, including zero costs.
Four one-bit examples approached the lower-bound limit. Runtime0.1967594s;
these are development identities, not workload savings or independent review.
