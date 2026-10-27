# Buy or retain witness labels when they simplify future inference

Codex (GPT-6), October26,2026. DEVELOPMENT; constructive interface extension
of forest_receipts.md. This uses ordinary cycle conditioning and feedback
vertex selection; no new graph-selection algorithm is claimed.

For receipt j, suppose a permitted service supplies an index i in I_j with
a warranted statement g_ji(x_i)<=b_j for the same source version. This is
one valid witness, not a promise of a unique winner or a deterministic
tie-breaking policy. Keep all old lower inequalities, add this one local
upper inequality, and remove receipt j's disjunction. The compatible set
remains exactly the sources satisfying the retained statements, under this
label contract. A guessed label without its warrant cannot be imposed.

Choose a set J of receipt vertices whose deletion makes the incidence graph
a forest. Once their labels are supplied, the forest construction computes
the full future-value interval with O(n+k) local LP calls. This interval is
conditional on the extra information; it need not equal the earlier union
of intervals. All chosen labels coexist at the fixed actual source.

If the original graph has cycle rank t, take any spanning forest and collect
the receipt endpoints of its t omitted edges. This chooses at most t
receipts. Their labels need at most sum_(j in J) ceil(log2 |I_j|) index
bits, plus identifiers, source versions, warrants and the actual purchase,
verification and retention costs. The procedure avoids enumerating the
2^t cycle branches after those observations. It does not establish that
buying them is cheaper than computation, direct queries or richer retention.

With unequal label prices, finding the cheapest receipt deletion set is an
ordinary weighted feedback-vertex problem with deletions restricted to one
bipartition. It is already as general as graph feedback vertex selection:
represent each original graph vertex by a receipt and each original edge
by a degree-two configuration vertex. Deleting receipts breaks all cycles
exactly when deleting the corresponding original vertices does. This is a
comparison reduction, not a new hardness theorem. A cheap spanning-forest
choice suffices for the stated at-most-t guarantee; optimal selection is
not supplied for free.

## What information is being purchased?

In the tight t-cycle example from forest_receipts.md, all old scalar
receipts are zero and the future minimum has2^t different possible values.
One binary witness label from one of each gadget's two receipts identifies
all t independent choices. Conversely, any binary-answer procedure that
must identify the exact future value in this family has a worst-case
transcript of at least t bits: fewer binary leaves cannot distinguish2^t
values. This is the standard decision-tree counting argument.

It is a lower bound for acquiring an exact answer through that binary
interface, not for computing the entire uncertainty set. The uncertainty
set can be computed without acquiring any label, and a direct future-value
query would answer the decision in one query if permitted. These different
information contracts must not be mixed in a claimed saving.

A yes/no query about one omitted edge has another complication: a negative
answer adds the strict inequality g_ji>b_j. Compact closed-polytope output
and endpoint attainment no longer follow automatically. The witness-index
contract above deliberately avoids that issue. An extension allowing
strict inequalities needs explicit feasibility and endpoint-inclusion
certificates; silently replacing > by >= is unsound.

The useful synthesis is a priced choice between keeping an anonymous scalar
receipt, retaining a small witness label with its warrant, and paying later
for the ambiguity it leaves. Its substantive algorithmic support comes from
the forest/range construction. Its practical economics and comparative
novelty remain open.
