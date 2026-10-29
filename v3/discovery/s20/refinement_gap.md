# A sharp computation-gap bound from a partial loss-cell signature

Codex (GPT-6), October29,2026 UTC. DEVELOPMENT, separate from A1.
This extends the decision-cell interface rather than the fixed V19 theorem.
It does not claim a new generic minimax or value-of-information principle.

## Joint uncertainty about the robust loss vector

Let K be the known attainable loss cells and P the possible cells, K subset P,
P nonempty. The true support J satisfies K subset J subset P and J nonempty.
For a fixed finite action set, let v_ja be the loss of action a in cell j.
Write W_a(J)=max_(j in J) v_ja. For K nonempty put l_b=max_(j in K) v_jb.
With K empty use l_b=-infinity solely in the formula below.

The earlier eta_a=max(0,u_a-min_(b!=a) l_b) is safe, but can be loose because
the same unknown cell can raise several actions' worst losses together.
The exact largest robust suboptimality of action a over bracket-compatible
supports is

    Gamma_a = max(0, max_(b!=a) max_(j in P)
                         [v_ja-max(l_b,v_jb)]).                 (R1)

For one action Gamma=0. For K empty, the expression in brackets is v_ja-v_jb.
This is a bound on W_a(J)-min_b W_b(J), not a bound on actual-state loss.

For the upper bound, choose a cell j attaining W_a(J). Then
W_b(J)>=max(l_b,v_jb), so W_a(J)-W_b(J) is at most the corresponding term
of(R1). Maximizing over b and zero proves the bound. For sharpness, choose a
maximizing pair(b,j) and set J=K union{j}. This is nonempty, has
W_b(J)=max(l_b,v_jb), and W_a(J)>=v_ja. Hence its actual suboptimality is
at least that term. Together with the upper bound this establishes equality.
If Gamma=0, every admissible support already realizes zero suboptimality.

With c possible cells and m actions, direct evaluation uses O(c*m^2)
rational comparisons and arithmetic, plus reading the cell losses. A witness
support of at most |K|+1 cells certifies any positive value. No enumeration
of all2^(|P|-|K|) possible supports is required. Source constraints may rule
out some of these supports, so this is sharp for the supplied signature
information, not necessarily for the original receipt model. Rational points
in the cells give an interval-bracket witness I union{q_j}; they do not by
themselves give an original hidden-source witness.

## A strict improvement and its ordinary interpretation

Take known loss cells(9,0) and(0,10), and one possible additional cell(12,13).
Then l=(9,10), u=(12,13). The earlier bound for action A is eta_A=2.
But the true worst-loss vector is either(9,10) or(12,13), so A is always
strictly better than B. Formula(R1) gives Gamma_A=0. This is not simply
statewise dominance: B is better in the known cell(9,0). The information
that the cell(0,10) is also attainable is necessary to this conclusion.

Thus one can certify that resolving the last cell cannot improve the chosen
fixed-model robust action, even though each worst-loss value is unresolved.
An ordinary calculation of these same joint maxima gives the same result.
The useful adaptation is to expose this certificate instead of demanding
completion of every range endpoint. A positive Gamma is only an upper bound
on a computation's possible benefit; it does not make that computation worth
its fee or show that the witnessing support is physically attainable.

Apply the fixed-model stopping contract from partial_decisions.md with Gamma
in place of eta. Do not apply it to a new observation, changed action class,
reuse value or a counterfactual change of source. For minimax regret, first
transform every cell vector to v_ja-min_b v_jb, then use(R1). Loss and regret
must not be mixed in either the known maxima or the unknown-cell term.

## Optimality is not safety or statistical calibration

Two cells(0,10),(10,0) make both deterministic actions minimax-optimal:
Gamma=0 when the support is known. Nevertheless either action can incur
loss and actual-state regret10. A numerical optimality certificate is not
a small-loss certificate. A valid upper bound on actual loss is u_a; for
actual-state regret it is the upper bound after the regret transformation.

If an upstream simultaneous coverage event E has probability at least1-delta,
and a possibly adaptive stopping rule returns an action with certified actual
loss at most a fixed gamma on E, with losses always in[0,M], then

    Pr(loss>gamma) <= delta,
    E[loss] <= gamma + delta*(M-gamma),  for0<=gamma<=M.          (R2)

Split the expectation over E and its complement to prove this. The gamma in
(R2) is an absolute loss bound, not Gamma from(R1). A random reported upper
bound cannot be substituted in the product formula without handling its
dependence on E. The simpler E[loss]<=E[reported_bound]+delta*M is valid
for nonnegative reported bounds whenever they bound loss on E.

Coverage must hold simultaneously across the selected time/source versions.
For instance, intervals which fail independently with probability1/100 each
have fixed-time99% coverage; stopping at the first failure through100 steps
fails with probability1-(99/100)^100, much larger than1/100. Conversely all
deterministic consequences of one genuinely covered source need no additional
query-count penalty. These are standard coverage and decision facts, as
credited in partial_decisions.md; no calibration method is implemented here.

Disposition: develop a stricter task-specific stopping interface and check it
against exhaustive support enumeration. Standalone novelty UNASSESSED;
no additional promotion credit or empirical fee claim.
