# A fallible proposed proof bank with a priced fallback guarantee

Codex (GPT-6), October26,2026. DEVELOPMENT derivation. This is a proposed
hidden-completion adaptation of ordinary learning-augmented primal-dual
covering; no novelty or independent-confirmation claim.

## Advice and benchmark

Keep the fixed proof procedures, monotone-CNF requests, unknown total checked
completion costs R_j, request fallback costs c_t and maximum clause width d.
Let a fallible model propose a fixed bank J of certificate procedures before
the stream. Its cost is evaluated using actual R_j, not predicted runtimes:

    A(J)=sum_(j in J) R_j + sum_(t: J does not satisfy phi_t) c_t.

This is a feasible hindsight plan if every selected R_j is finite: purchase
the bank once and fall back on requests it does not discharge. It may be
arbitrarily worse than OPT. If a proposed procedure never completes, A(J)
is infinite and its advice-specific guarantee is vacuous. The robust bound
below still applies. Source applicability is encoded in the supplied phi_t.
Advice acquisition and testing the hitting relation remain extra costs.

Choose epsilon in(0,1]. At an unresolved request, first test whether J hits
every clause of phi_t. If yes, call it a bank request. On each selected
unsatisfied clause C, designate any j in J intersect C. Increase y_tC while
advancing that designated procedure at rate1/epsilon and every other member
of C at rate1. Use total request dual cap c_t. If J fails to hit some clause,
call it a fallback request: advance every selected-clause procedure at rate1
and use cap epsilon*c_t. At exhaustion pay c_t if still unresolved.
The test concerns the proposed bank, not whether its proofs are completed.

## Two simultaneous bounds

All procedure progress rates are at least1 whenever a dual variable involving
that procedure grows. Completed procedures never appear in a later selected
unsatisfied clause. Hence sum_(t,C:j in C)y_tC<=R_j, and both types of request
respect sum_C y_tC<=c_t. Thus Y=sum y_tC<=OPT by the same covering dual.

For a bank request, work rate is at most d-1+1/epsilon and any fallback is
at most its total dual mass. Its combined bill is at most(d+1/epsilon)Y_t.
For a fallback request, work is at most dY_t, while a paid fallback at the
cap equals Y_t/epsilon. The same bound follows. Therefore

    B <= (d+1/epsilon)*OPT.                         (PA1)

Assign each bank-clause dual increment to its designated member of J. That
procedure received1/epsilon times the assigned mass, so the total mass
assigned to j is at most epsilon*R_j. Fallback-request mass is at most
epsilon*c_t. Summing yields Y<=epsilon*A(J), therefore simultaneously

    B <= min((d+1/epsilon)*OPT, (1+d*epsilon)*A(J)). (PA2)

When the proposed bank is an optimal plan, the consistency factor is
1+d*epsilon; arbitrary advice retains robustness d+1/epsilon. At epsilon1
this is the original d+1 guarantee. The result is pathwise and requires no
accurate probability or completion-time forecast. A useful model needs only
to nominate a cheap reusable bank with appropriate request coverage; the
certificate checker still determines mathematical correctness.

The nonuniform virtual-credit implementation stops at the next actual price
threshold divided by the active procedure rate. It executes all tied due
instructions. No future completion length is exposed. The proof applies to
paid generation and verification as specified in proof_interface.md.

## Scope and ordinary controls

This is not a new principle of trustworthy advice. The close comparison is
learning-augmented online covering with known purchase prices, especially
primal-dual algorithms that favor advised sets. The possible incremental
content is a completion-only, persistent proof-bank implementation of that
tradeoff, charging unfinished work and complementary requirements. A full
ordinary implementation of the same scheduler ties. Arbitrary SAT solving,
state eviction, schedule-dependent runtimes and unpriced controller overhead
remain outside the benchmark.

Predicting only the cheapest individual proof does not imply a nearly-one
ratio to OPT when the future horizon might be short: the all-fallback plan
can be cheaper. A(J) deliberately includes the bank purchase and requests
outside its coverage. Choosing epsilon after seeing evaluation results would
be development selection, not confirmation. No numerical probe has yet been
run for(PA2); the earlier frozen scheduler used epsilon1 only.
