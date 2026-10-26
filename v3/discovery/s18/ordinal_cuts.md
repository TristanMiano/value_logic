# Exact fault-budget preference warrants by cuts

Codex (GPT-6), s18 DEVELOPMENT. Ordinary directed minimum cuts and max flow
are the mechanism. The candidate increment concerns the precise report and
decision contract; its close literature comparison remains unfinished.

Primary comparison update: the flow relation itself, including its strict
transitivity, is established in [Bubboloni--Gori2018](https://arxiv.org/abs/1606.03898)
and earlier work they credit. [Gori2024](https://doi.org/10.1016/j.mathsocsci.2024.05.003),
Sections4--5, explicitly interprets edge-disjoint paths as independent
dominance arguments and discusses erroneous reports. This substantially
narrows any novelty claim: neither flow ranking nor its robustness
interpretation is new here. The remaining screen is the exact shared-report
countermodel contract and its online consequence, compared with those
antecedents and robust ordinal regression.

There are d named alternatives with fixed unknown real utilities, ties
allowed. Each retained report names a nonempty available set S_t and an
asserted optimal member i_t. At most C reports are false. A report is false
when some j in S_t has u_j>u_(i_t); its many pairwise assertions share one
fault charge. No numeric utility observations are assumed. An all-equal
utility vector always makes every such report true, so these weak reports
alone cannot make the utility source inconsistent.

## An exact countermodel characterization

For distinct a,b, let kappa(a,b) be the minimum number of false reports
among utility vectors satisfying u_a<u_b. It suffices to consider utilities
in{0,1}, with a low and b high. Given any real countermodel, put a threshold
strictly between their utilities. Every report made false by thresholding
already had a strictly higher member than its reported winner. Conversely,
a binary assignment is itself a real countermodel.

Thus kappa(a,b) is the minimum, over low sets L containing a but not b, of
the number of reports whose winner lies in L but whose available set has
at least one member outside L.

Create one auxiliary vertex r_t per report, an arc i_t->r_t of capacity1,
and arcs r_t->j of capacity m+1 for j in S_t minus{i_t}, where m is the
number of reports. Take a minimum directed a-to-b cut. Its low side is L.
A minimum cut never pays m+1 because a cut of cost at most m exists. It
pays exactly one for each report crossing from a low winner to a high
alternative, by placing that report node high; other report nodes can be
placed without a charge. Therefore its value is exactly kappa(a,b).

Consequently

    every source with at most C false reports has u_a>=u_b
        iff kappa(a,b)>C.                                  (O1)

The minimum cut supplies a countermodel when the test fails. Integral
max flow supplies C+1 paths with distinct report-capacity edges when it
passes. This avoids charging one bad winner report once for every pair
it mentioned. Opposite warrants can both hold; they then certify a true
utility tie, rather than a contradiction.

For an available set S, a fixed a in S is guaranteed optimal exactly when
(O1) holds against every other b in S. Only these d-1 queries are needed
for a proposed action; all-pair reconstruction is optional. This is a
worst-case warrant under an explicit hard budget, not a learned probability.

## A stronger ordinary online score

Directed minimum-cut values satisfy

    kappa(a,c)>=min(kappa(a,b),kappa(b,c)).

Every cut separating a from c puts b on one side or the other and therefore
separates one of those pairs. The same short transitivity proof as for
strongest paths shows that kappa(a,b)>kappa(b,a) defines a strict partial
order. Use any total extension to select the highest-ranked available item.

If u_a<u_b, thresholding the actual utility vector gives a cut of cost at
most the actual corruption count C, so kappa(a,b)<=C. If a truly better
item has been reported over b on more than C distinct rounds, every
a-to-b cut pays for all those reports, so kappa(a,b)>C. Charging mistaken
uncorrupted rounds to the winner/proposal pair gives the same bound

    binom(d,2)*(C+1)+C

on suboptimal choices without knowing C. Unlike the bottleneck-path score,
the cut score can combine several independent report paths. Its computation
and graph storage can be larger: all-pair max flows on the report graph
are polynomial but are not the O(d^3) path kernel. A workload comparison
is needed before preferring one for a bounded reasoner.

With pair-only reports, the graph reduces to ordinary parallel directed
edges with capacities equal to report counts. Two edge-disjoint a-to-b
paths can warrant a>=b at C=1 even though each individual edge has count1
and the strongest bottleneck path has strength1. For example reports
a>=x, x>=b, a>=y, y>=b have kappa(a,b)=2. All four reports refer to
separate rounds; duplicating one report would not provide this guarantee.

## Pairwise cut values are not sufficient for arbitrary future updates

On four alternatives a,b,c,d, compare two pair-report graphs. The first is
the cycle a-b-c-d-a with capacity3 in EACH direction on each cycle edge.
The second is the complete graph with capacity2 in EACH direction.
Every directed pair minimum cut is6 in both graphs.

Now add10 new reports in each direction of a-b and c-d. In the first graph,
the a-to-c cut{a,b}|{c,d} still costs6. In the complete graph it costs8,
and every separating singleton or triple costs at least16; the other
two-versus-two cuts cross one of the added heavy pairs. Thus the new
a-to-c minimum cut is8. At hard fault budget7 the second updated source
warrants u_a>=u_c and the first does not.

This gives a small exact update failure for a summary that preserved ALL
current pairwise fault-budget warrants. It is not a lower bound against
every compressed graph representation, nor a claim that cut-equivalent
structures were previously thought update-complete. The relevant lesson
is to retain enough joint cut information for the promised future duty.
