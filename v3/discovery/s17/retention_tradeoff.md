# Stronger retention and acquisition controls

Codex (GPT-6), October 24, 2026 UTC. DEVELOPMENT; consequences and limitations
of the bounded contribution, not additional requirements for its theorem.

## Uniform approval of an entire target subspace

If the only duty is to bound the edited value uniformly over every unit target
in the retained subspace, the full directional geometry is unnecessary after
acquisition. Let lambda_max and lambda_min be the extreme eigenvalues of C.
Because every U_t and L_t is an increasing scalar function of C, and their
eigenvectors are those of C, the core theorem gives

    sup_(compatible M,N, unit c) F(N;Wc) = upper(lambda_max,1,e),
    inf_(compatible M,N, unit c) F(N;Wc) = lower(lambda_min,1,e).

For example, c^T U_t(C)c <= U_t(lambda_max) for every t. Infimizing t
gives the upper inequality; choosing a largest-eigenvalue eigenvector and
using its finite endpoint witness gives equality. The lower proof reverses
the corresponding inequalities and uses a smallest-eigenvalue eigenvector.
No minimax interchange is assumed. Thus a scalar extremal-eigenvalue receipt
suffices for this uniform duty. Acquiring that eigenvalue is not thereby free
or equivalent to one ordinary quadratic-value query.

The full block instead supports directional decisions for later declared
targets, including targets chosen after its acquisition. Its deterministic
bounds hold for all such choices, with the appropriate target and edit warrant.
This is a retention capability, not evidence that buying every block entry
is economical for a single known target.

## One targeted old-value query can settle the worked upper decision

The existing [variational witness](../s16/query_witness.md) is a particularly
strong control. With a=1+t, d=t-E-E/t>0 and any proposed z,

    F(N;Wc) <= a q(z)+(a/d)||c-z||^2,
    q(z)=z^T C z.

Only an upper receipt for this one old value is needed for an upper-threshold
decision. A second query is useful when both interval endpoints are requested;
three-query polarization is not a necessary acquisition cost for this duty.

In the cancellation example take t=100, E=9, d=9091/100, c=(1,1)/sqrt(2)
and z=(19/20,1/80)/sqrt(2). Query the rational unnormalized vector
y=(19/20,1/80). The unfinished primal solution used in acquisition.md gives

    q(y) <= (19/20)^2/1600+(9/10)(1/80)^2 = 451/640000.

Scaling this truthful receipt by one half and substituting the proposed z
gives the exact upper bound

    45551/1280000 + (5050/9091)(6257/6400)
       = 6733674141/11636480000 < 3/5.

The margin is 248213859/11636480000. This uses one old-value acquisition
with a proposed primal vector, not the block checker's three-query adapter.
It follows by the displayed rational arithmetic and the existing variational
inequality; no new numerical experiment is needed. The proposal was selected
using the exposed development example, so this is not a measured learning or
query-selection result. Producing such a good proposal generally has a cost.

This control preserves the useful decision consequence but weakens any claim
that its three block queries are a minimal or favorable purchase. The block's
case must rest on its exact information characterization and reuse for later
directions/budgets, or on an explicitly priced workload where it repays its
cost. N16-C/v1 does not presently claim such an economic advantage. The same
ordinary variational witness is part of the proposed synthesis's conventional
machinery, and should be offered when it is the cheaper sufficient interface.
