# Strong ordinary control: interval bottleneck paths

Codex (GPT-6), October 28, 2026. P3-11-A1 reconstruction. This is an
equivalent ordinary derivation, not an additional novelty claim.

## General finite-path identity

Let a finite directed acyclic graph have source s, sink t, and each edge e
have a nonempty attainable interval [l_e,u_e]. A path chooses one value in
each of its edge intervals, independently along that path, and reports their
minimum. Paths contain at least one edge. Define

    M_e = max_(s-t paths P containing e) min_(h in P) u_h,

omitting e when it lies on no complete path. Then the set of every attainable
path report, across all paths and all such edge-value choices, is exactly

    union_e [l_e,M_e], discarding intervals with l_e>M_e.

For necessity, choose an edge attaining the minimum q on a realizing path.
Its lower bound is <=q, and every path upper endpoint is >=q, so q<=M_e.
For sufficiency, a path attaining M_e exists because the graph is finite.
Choose q on e and each other edge's upper endpoint. Since M_e<=u_e and all
other upper endpoints are >=M_e, this choice is allowed and its minimum is q.
This proof also handles equal values and degenerate intervals. It does not
need all edges' values to be simultaneously realizable under one global
physical source; it needs only the indicated pathwise independence.

M_e is an ordinary forced-edge bottleneck max-marginal. Compute the widest
prefix value F(v) and suffix value B(v) with max over paths and min along a
path. Their neutral value is +infinity at s and t; unreachable vertices are
absent. For e=(v,w),

    M_e=min(F(v),u_e,B(w)).

Any compatible prefix and suffix concatenate with e. Acyclicity prevents
their sharing another vertex: a shared vertex would create a directed cycle
through e. Taking maximizing prefix/suffix paths proves attainability and
the reverse bound. One topological forward/backward pass and an edge scan
therefore cost O(|V|+|E|) scalar comparisons, apart from constructing the graph
and sorting/merging its emitted intervals. This is a standard path-computation
specialization, not a new widest-path algorithm.

## Exact V19 reduction and the storage distinction

Use layer i and a receipt subset S already assigned after the first i blocks
as vertices. There is an edge from (i-1,S) to (i,S union T) for each T disjoint
from S whose local slice Q_i(T) is nonempty. Assign that edge the local
interval [ell_i(T),u_i(T)]. The source is (0,empty), the sink is (n,K).
Every complete path is exactly a partition of receipts among blocks, and
every such partition has one path. A path uses one local slice per block;
its independent LP interval choices are realizable by independent block
vectors. Repeated use of the same local label on different alternative
edges does not require inconsistent simultaneous choices on one path.

There are (n+1)*2^k possible vertices and at most n*3^k edges. For each receipt
at a layer choose already in S, newly in T, or still unassigned. Edges with
the same local label (i,T) have the same lower endpoint. Their intervals
therefore union to one interval with greatest upper endpoint, or none:

    M_i(T)=max_(S disjoint T) min(F(i-1,S),u_i(T),B(i,S union T)).

This equals the clipped outside cap in AR1. Hence the n*2^k output bound is
the aggregation of ordinary edge max-marginals by their shared local label.
The graph need not be retained explicitly: generate each outgoing subset
transition during the layer scan, and store only vertex values, maximizing
splits and local-label aggregates. This yields O(n*2^k) scalar entries with
O(n*3^k) transition work. LP inputs, exact bit costs and certificate/source
storage remain separate, as in the fixed claim.

An ordinary implementation of this reduction ties V19 in every output and
in these resource bounds. The interval spectrum identity, max-marginal idea,
and subset-DAG trick should not be described as exclusive Value Logic machinery.

## Closest primary comparison and consequence for novelty

[Abbas and Swoboda (2019)](https://arxiv.org/pdf/1904.08080), Appendix 6.2,
including the displayed Min Marginals BMRF algorithm, was additionally read
here. It computes bottleneck-related min-marginals with forward/backward
path quantities and threshold updates for its mixed bottleneck/linear-cost
model. The pure bottleneck case is simpler. This reinforces the established
status of constrained bottleneck marginals; the earlier Section 3--4.2 read
was not enough to support a claim that such marginals were absent. No seismic
experiment or mixed-objective performance claim is imported.

The exact path identity above is reconstructed directly, not claimed as a
new theorem from that paper or as proof that no previous paper states it.
It sharpens the routine-specialization risk. The remaining V19 contribution
event can only concern the explicit end-to-end mathematical contract from
shared interval optimum receipts over ordinary polytopic blocks to the
complete future scalar image, with the parameterized resource guarantee,
complete rational certificates, reconstructable sources, output-size limit
and a consequential noisy example. It cannot claim new max-marginal inference.
Whether that specific adaptation is moderately novel is a substantive expert
judgment, not something more tests or more formal lemmas can decide.
