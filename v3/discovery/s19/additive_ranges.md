# A separate additive-readout consequence of the component reduction

Codex (GPT-6), October26,2026. DEVELOPMENT derivation, unimplemented and
unassessed for novelty. This is not a prerequisite for V19-R/v1.

Keep the product source and k interval minimum receipts of claim.md, but
ask for the range of F(x)=sum_i f_i(x_i), with affine rational f_i. The
minimum-specific anchor formula does not apply. Global endpoints alone
are easy by min-sum/max-sum subset partitioning, but they can erase gaps.

The feasibility-type reduction in fiber_components.md suggests a finite-
parameter whole-range algorithm even here. Compute every local slice's
feasibility and endpoints ell_i(T),u_i(T), using at most2*n*2^k LPs.
If any Q_i(empty) is empty, the global source is empty. Otherwise define
F_i={T:Q_i(T) nonempty}. Keep k+1 labeled bins of each type that has more
than k bins, and keep all bins of smaller types. The reduced graph has
at most N=(k+1)*2^(2^k) bins and N^k feasible receipt assignments.

Build its one-receipt-move graph and connected components. The established
type-capping argument preserves source components. Small types retain
their actual labels. For a large type, any injection of its occupied
receipt blocks into the original bins is connected to any other injection:
there is always a spare bin, and whole feasible blocks can be moved through
it one receipt at a time. Thus such relabelings stay inside one component.

For each reduced assignment alpha, let T_1,...,T_r be its nonempty blocks
of a given large type. Optimize their placement in the original bins of
that type by a rectangular minimum-cost matching, with edge costs

    ell_i(T_j) - ell_i(empty).

Start with the baseline sum_i ell_i(empty); add those matching optima and
the fixed occupied-bin corrections for small types. This is exactly the
smallest F over all original assignments represented by alpha. For the
largest value, use u_i instead and maximum-cost matchings. Empty bins retain
their empty-slice endpoints; they must not be dropped from the numerical
objective. Matchings enforce distinct bins for distinct occupied blocks.

Take the smallest lower and largest upper endpoint across all reduced
assignments in each graph component. The represented original cells cover
that source component, which is compact and path connected. Therefore its
continuous scalar image is the entire closed interval between these extrema.
Merge the resulting at most k! intervals. Local extremizers, matching
assignments and the known finite cell paths provide constructive witnesses;
an efficient arbitrary-q recovery routine is not developed here.

This yields a very coarse f(k)*poly(input size) algorithm using the ordinary
assignment/matching machinery, in addition to local rational LP bit costs.
It is not an attractive practical bound: the type graph is doubly
exponential in k. It does show why numerical source vectors cannot simply
be discarded in the earlier topological reduction; matching preserves
their distinct costs. It does not extend to sums of future minima, whose
terms couple generators, or to a joint value polytope.

**Disposition:** retain as an optional structural observation. Do not add
it to the promotion event or start a verification campaign. Its dependence
on the coarse component reduction and ordinary weighted matching needs
a separate proof and close comparison before any novelty estimate.

Two analytic sanity cases illustrate why labels and spare bins matter.
With x_1,x_2 in[0,1], receipts min_i x_i=0 and min_i(1-x_i)=0 force
(x_1,x_2) to be(0,1) or(1,0). The additive readout x_1+2*x_2 has range
{1,2}. There is no spare bin, and those labeled assignments stay separate.
With three such coordinates, the same receipts describe the cube's
six-edge cycle. The readout x_1+2*x_2+4*x_3 has range[1,6]: the source
is connected, and its smallest and largest values occur at the indicated
weighted binary vertices. These are hand-derived fixtures, not an
executed validation panel.
