# Retaining complementary upper and lower certificates

Codex (GPT-6), October25,2026 UTC. DEVELOPMENT; broad constructive branch.
This develops the cost boundary in[witness_retention.md](witness_retention.md)
using the existing paid repair archive as a possible natural source.

For a future request q, retained primal witness j supplies a checked upper
value U_j(q), and retained proof i supplies a checked lower value L_i(q).
With tolerance tau_q, a pair closes the request when

    U_j(q)-L_i(q)<=tau_q.

The witness must remain feasible and the lower proof must remain valid under
the request's source/weight contract. A finite bank can be checked beforehand;
no unknown validity probability is required in this first specialization.
Let f_q>=0 be the fee avoided by a cache closure, excluding bank evaluation
and maintenance which must be charged separately.

For retained sets J,I the gross avoided-fee objective is

    F(J,I)=sum_q f_q * 1[exists j in J,i in I with a closing pair]. (P1)

Baseline certificates can be included as always-available elements. With no
baseline closures, one witness and one proof can each have zero utility alone
and positive utility together. Thus F need not be submodular on the combined
bank. The independent-box/Pandora reduction does not resolve this logical
complementarity.

## A useful conditional structure

For fixed J, each proof covers the requests for which it closes with some
retained witness. Hence F(J,.) is ordinary weighted maximum coverage and is
monotone submodular. The same holds with I fixed. This is a two-sided
coverage objective, not joint submodularity.

If at most k_W witnesses and k_L lower proofs can be retained, enumerate all
witness subsets of size at most k_W and, for each, greedily add k_L proofs
by marginal covered fee. Keep the best complete pair of sets. The result is
at least alpha_(k_L)=1-(1-1/k_L)^k_L times the best feasible bank, since one
enumerated witness set is the globally optimal one and ordinary greedy has
that guarantee on its proof side. This is practical only for a genuinely
small witness quota; enumeration, coverage construction and all forecast
evaluation are paid work. Swapping the sides can be cheaper. For small quotas
on both sides, exact enumeration is a useful strong control.

The result is an immediate composition of enumeration and maximum coverage,
not a proposed new general approximation algorithm. It gives an explicit
alternative to claiming that individual-receipt greedy solves the problem.

## Reducing gaps can fail to close valuable decisions

The continuous gap-reduction surrogate is more tractable: improving the best
upper bound and best lower bound gives a sum of maximum improvements, and
truncating at the original gap preserves monotone submodularity. But a fee is
saved only after the gap crosses the requested tolerance.

For a concrete failure, take three requests for which witness A removes99%
of the gap, each needing its own lower proof to remove the last1%. Separately,
take two requests for which witness B removes50% and one shared lower proof C
removes the remaining50%. Give every request fee1 and allow two retained
receipts in total. Greedy normalized gap reduction first selects A with gain
2.97, then B or C with gain1 rather than an A-partner with gain.01. It closes
zero requests. Selecting B,C closes two. Every request can be closed by a
two-receipt pair; the failure is not caused by an intrinsically impossible
target. Gross fee coverage needs its own objective and strong controls.

## Scope of a natural development probe

The s05 checked repair archive already contains29 feasible assignments and18
negative proof trees, with known source/weight meanings and an80-request
exposed stream. Inspect that interface before deciding a probe. Reuse of
historical receipts is allowed for DEVELOPMENT and must not be described as
new source purchases, independent evidence, or a fresh observed workload.
Compare joint selection, the full admitted cache, individual/gap surrogates
and any available ordinary persistent solver. Equal selection rules tie by
construction. A capacity-constrained cache may be useful without beating
every conventional retention method, but storage and query costs still matter.

The bounded exposed-bank probe is now complete; see
[findings](retention_findings.md). It confirms eleven genuinely complementary
pairs in each representation and a small source-wise exact allocation problem.
This provides a natural finite instance, not a general economic contribution.
