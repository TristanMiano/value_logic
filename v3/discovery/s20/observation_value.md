# Computation and observation have different stopping bounds

Codex (GPT-6), October29,2026 UTC. DEVELOPMENT adapter; standalone novelty
UNASSESSED. Established robust information acquisition is the starting point.

## Finite signal contract

Use the loss-cell signature K subset J subset P from refinement_gap.md,
where J is nonempty. A specified truthful observation returns a signal s(j)
determined by the actual cell. The decision maker may choose any one of the
m declared deterministic actions independently for each signal. The observation
has a fixed fee c in the same units as loss. Its acquisition, representation
and policy costs must be added when used; they are not estimated by this model.

For a completely known support J, define

    B(J) = min_a max_(j in J) v_ja,
    Q(J) = max_(s: J_s nonempty) min_a max_(j in J_s) v_ja.      (O1)

The second expression is exactly the best worst loss of a signal-contingent
policy. For any policy each branch is at least its branch optimum; choosing
each branch's minimizing action achieves their maximum. This uses the full
Cartesian policy class and cannot be imported to policies with shared memory,
fairness, randomization or other restrictions without redoing the optimization.
Ignoring the signal is allowed, so0<=B(J)-Q(J). Fee-adjusted gain is B-Q-c.

For the two-cell matrix(0,10),(10,0), constant actions have worst loss10 and
a signal distinguishing the cells permits loss0. Thus observation value is10
although additional computation of the already known support has value0.
Neither number is an expected-value claim or a probability of a state.

## Safe coarse bounds when the support is incomplete

Both B and Q are monotone in the support. When K is nonempty,

    max(0,B(K)-Q(P)) <= B(J)-Q(J) <= B(P)-Q(K).                (O2)

If K is empty the lower bound is0; replace Q(K) in the upper bound by the
minimum entry of the possible loss matrix. A policy optimized on P is usable
already: its worst loss on J is at most Q(P). Thus a positive B(K)-Q(P)-c
certifies an implementable improvement in the robust criterion over even
the best constant action for J. It does not prove pointwise improvement on
every actual state. Conversely an upper value at most c rules out a strict
fee-adjusted gain for this fixed observation contract.

## Sharp upper value by ordinary subset covering

There is a stronger upper bound, exact over all supports between K and P:

    U = max_(K subset J subset P, J nonempty) [B(J)-Q(J)].      (O3)

Let V contain all finite cell-loss entries. For candidate thresholds b,t in V,
ask whether some support satisfies B(J)>=b and Q(J)<=t. For each signal s
and possible branch action h, form its allowed cells

    A_sh(t) = {j in P_s : v_jh<=t}.

This option is legal precisely when K_s subset A_sh(t). Its coverage mask
contains the constant actions a for which some j in A_sh(t) has v_ja>=b.
Choose one legal option per signal. The threshold pair is feasible if and
only if the union of those coverage masks contains all m constant actions.

Forward proof: a feasible J has a branch action h with all its signal cells
at loss at most t; enlarge J_s to A_sh(t). This preserves the known cells and
cannot reduce any constant action's worst loss. Every constant action has
a cell attaining at least b, so the option masks cover all actions.
Reverse proof: use J equal to the union of the chosen A_sh(t). It contains K;
full action coverage implies J is nonempty; the chosen policy has worst loss
at most t, and every constant action has worst loss at least b. Hence B>=b,
Q<=t as required. Empty possible signal branches may take an arbitrary action.

An ordinary multiple-choice subset-cover DP decides the mask union in
O(s*m*2^m) transitions after option masks are formed. Keep one backpointer
per reachable mask to recover a policy and its allowed-cell support. Enumerate
the at most |V|^2 threshold pairs and maximize b-t over feasible pairs.
This maximum equals U: every feasible pair has a realizing support with
gain at least b-t, while an optimal support has B and Q in V and supplies
one of the enumerated pairs. Direct option construction costs O(cells*m^2)
per pair; rational bit costs and policy output are separate. This is exponential
in action count, not report count, and is not a universal efficient policy learner.

The returned maximizing support is allowed by the signature alone; the
original receipt geometry can rule it out. Consequently U is still only
an upper bound for that richer model. A low upper value can safely reject
buying this observation, but a high upper value is not a recommendation to buy.
Do not treat it as a distribution over supports or an original-source witness.

## Closest established framework and reading scope

[Paradiso, Georghiou, Dabia and Tonissen, arXiv2208.04115v1](https://arxiv.org/pdf/2208.04115)
already formulate robust decision-dependent information discovery as nested
worst-case, recourse and compatible-uncertainty optimization. Read introduction,
section2/equations1a--1b, the section3.1.1 deterministic-cost qualification,
Lemma1 and its full EC.1 proof, plus the adjacent finite termination arguments.
Their monotonicity proof shrinks the compatible uncertainty set when more
coordinates are observed. This is a strong conventional antecedent; the
present finite signal value is a specialization, not a new information principle.
The remaining algorithmic sections and empirical comparisons were not audited,
and the subsequently published version was not treated as identical proof text.

The threshold-cover calculation adapts standard finite max/min and subset-DP
machinery to an uncertain support signature. Its standalone contribution status
is unassessed. It is useful here because it provides the correct observation
counterpart to a computation-gap certificate without confusing their scopes.
