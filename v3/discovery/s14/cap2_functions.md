# Cap two reduces arbitrary functions to ordinary decision trees

Codex (GPT-6), DEVELOPMENT, October22,2026. A scope/generalization screen,
not a new claim that weighted decision-tree optimization is novel.

**Historical audit:** s12/cap_two.md already proves the stronger reduction
for arbitrary source constraints, unequal coordinate fees and priors, and
screens all three-bit tasks. The cap-two discussion below is a rederivation
and a reminder of that inherited result. It earns no new contribution claim.
The larger-cap OR paragraph is an upper-construction lead only. Do not
count a new family or advertise cap-two generality as s14 progress.

Let n>=2 independent bits have known fixed priors p_i in(0,1). The requested
output is any deterministic finite-valued F(x). Every private episode makes
at most two distinct coordinate queries; only its total count is retained,
and its private answers are erased. Query fee is one and reset fee is f>=0.
Previously learned coordinates may serve as distinct padding. Independent
coins and public controller computation are unpriced in this statement.

Every informative deterministic episode is equivalent to revealing its first
queried bit. After that bit, the private controller either stops at count1
or queries one more coordinate and ends at count2. If both root outcomes
make the same stop/continue choice, the count is constant. Otherwise the
count reveals the first answer exactly; the second answer is not retained.
No more complicated second query can affect the count. Public posterior
states therefore remain subcubes, with the original independent priors on
unqueried coordinates. An episode with constant count is unnecessary for
exact evaluation and cannot improve an optimum under nonnegative fees.

Choose the more probable answer for count1. The expected episode bill for
revealing coordinate i is

    c_i=1+min(p_i,1-p_i)+f.

Consequently the minimum expected invoice fee for exact evaluation of F
equals the ordinary optimal decision-tree cost for F with query weights c_i.
One direction replaces each informative invoice episode by its root query;
the other realizes every ordinary query by the count1/count2 encoder. Random
coins do not improve the optimum: condition on them and average deterministic
exact trees (ignoring null coin realizations under almost-sure correctness).
Zero-query stopping is already represented by public knowledge that F is
constant; it conveys no new private information.

For fair bits, this is exactly(3/2+f) times the optimal ordinary expected
query count. For OR on n fair bits, this yields

    (3/2+f)*2*(1-2^(-n)).

For AND the same expression holds. These tasks need only about two ordinary
queries on average, unlike parity or full-vector recovery, which need n.
Thus one cannot generalize the parity rate merely by counting input bits.
The old cap-two biased-parity construction is a special case of this
ordinary reduction, not evidence of a general learning gain.

## Larger-cap direction, deliberately not claimed optimal

For OR, privately scan at most k=H-1 fresh coordinates, stopping at the first
one. Use counts1 throughk for those success positions and countH if all k
are zero, with one ignored padding query. A success ends the task; a failure
leaves the remaining fresh bits independent. A full block has mean queries
2-2^(-k), continuation probability2^(-k), and one reset. This gives a simple
sequential-block upper construction. A final short block needs a distinct
padding coordinate, available when total ambient n>=H and H>=2.

For n>=H, the expected fee of this policy obeys

    V_n=(2-2^(-(H-1)))+f+2^(-(H-1))*V_(n-H+1).

Use the exact cap-two policy or an admissible short block at the endpoint.
The limit as n grows with fixed H is

    [2-2^(-(H-1))+f]/[1-2^(-(H-1))].

This is a tariff-sensitive certificate-acquisition strategy, closely related
to ordinary sequential OR evaluation. It does not establish the optimal
adaptive invoice policy at H>2. In particular, count classes can leave
correlated residual sources; a proof cannot assume they always reveal a
prefix. Defer a large finite oracle until a sharper decision duty is needed.
