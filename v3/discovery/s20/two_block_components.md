# A sharp component bound for two independent source blocks

Codex (GPT-6), October 28, 2026. DEVELOPMENT. New derivation, separate
extension to V19-R/v1; no readiness or confirmation is inferred from it.

## Claim and upper-bound proof

With n=2 source blocks and k receipts under the convex-slice contract, the
compatible source has at most binom(k,floor(k/2)) connected components.
Consequently every continuous scalar readout has at most that many interval
components in its image. This improves the general k! source bound and the
2*2^k scalar-minimum bound in this case. The count is sharp, including with
full-dimensional rational source polytopes and nonzero observation widths.

Let K be the receipt set and H the subsets S for which both Q_1(S) and
Q_2(K minus S) are nonempty. The cells

    C_S = Q_1(S) times Q_2(K minus S),    S in H,

are nonempty compact convex sets covering the source. If S is a subset of T
and both belong to H, their intersection is

    Q_1(T) times Q_2(K minus S),

which is nonempty. Therefore cells indexed by comparable subsets lie in
the same source component. Pick one cell from each component. Its indices
are an antichain in the Boolean lattice on k elements. The classical
Sperner theorem bounds its size by binom(k,floor(k/2)). We import Sperner's
theorem; the application to these source cells is the proposed adaptation.

Compactness and the finite convex cover ensure that the source components
are compact and path connected. A continuous real-valued image of each is
a closed interval, possibly a singleton. Distinct source components can
have overlapping images, so this is an upper bound on scalar components,
not an assertion that arbitrary readouts distinguish them.

For k=0 there is one product cell and the bound is one. An empty source
has zero components. This proof does not require affine objectives, only
convex local slices and compactness for the closed-interval statement.

## Exact sharpness

For k>=1 put r=floor(k/2). Let

    B_1={x in [0,1]^k : sum x=r},
    B_2={y in [0,1]^k : sum y=k-r},

and require min(x_j,y_j)=0 for every j. Their supports are disjoint and
have at least r and k-r members, respectively. Hence they are complementary
Boolean vectors, with exactly binom(k,r) choices for x. These source points
are disconnected. The readout f_1(x)=1+sum_(j=0)^(k-1) 2^j*x_j and the
constant f_2=2^k+2 give that many distinct values of min(f_1,f_2).
This extends the even-k witness in s19/output_size.md to the sharp upper
bound. The binary encoding is elementary, not a new combinatorial device.

## Full-dimensional, nonzero-width sharpness

For k>=2 set epsilon=eta=1/[16*(k+1)*2^k]. Replace each equality defining
B_1,B_2 by a band of half-width eta and retain the coordinate boxes. Use
receipt bands [0,epsilon]. These polytopes are full dimensional.

If S is the set of receipts assigned to block 1, its sum upper bound is
k-|S|+|S|*epsilon. Its required sum lower bound r-eta forces

    |S|*(1-epsilon) <= k-r+eta.

Since eta+(k+1)*epsilon<1, this implies |S|<=k-r. Applying the same argument
to block 2 gives k-|S|<=r, hence |S|=k-r. Every such S is feasible, using
the complementary Boolean pair. No feasible assignment has another size.

On C_S, block 1's coordinates in S are at most epsilon. Every coordinate
outside S is at least 1-eta-|S|*epsilon: subtract the upper bounds for all
other coordinates from the sum lower bound. Thus the weighted readout
differs from the Boolean value for K minus S by at most

    (2^k-1)*(eta+k*epsilon) < 1/16.

Distinct Boolean values are different integers, so these image intervals
are separated by a gap greater than 7/8. Each cell contains an interior
point of all its relevant inequalities: coordinates epsilon/2 in S and
1-epsilon/2 outside S have sum within eta of the target (the parity
difference is at most one), and the analogous block-2 point works. Small
perturbations preserve feasibility and change f_1. Each image therefore
has positive width. There are exactly binom(k,r) nondegenerate disjoint
closed intervals and the same number of source components.

The small tolerance has O(k+log(k+1)) encoding bits. This is an existence
construction; it is not a claim that a fixed noise tolerance independent of
k permits exponentially many resolvable components. All guarantees remain
conditional on the supplied two-block model. Adding an unmodelled third
block can change the prediction set, as the separate simplifying-control
example demonstrates.

## Pending assessment

The upper proof is short once the comparable-cell intersection is noticed.
A close primary comparison is required before treating it as a moderately
novel contribution. The new sharp bound may strengthen a useful synthesis;
it does not replace V19-R/v1's event with an easier target or automatically
raise its readiness. Generic Sperner, set-membership prediction and
inside-outside machinery remain credited antecedents.

The original Sperner paper is [E. Sperner (1928), *Ein Satz ueber Untermengen
einer endlichen Menge*](https://doi.org/10.1007/BF01171114). Its archive page
was inaccessible here; [Das, Gan and Sudakov (2013), section 1.1](https://arxiv.org/pdf/1302.5210)
states the classical antichain bound used above. No claim to a new Sperner
inequality is made. [Gorski, Pfeuffer and Klamroth (2007)](https://www2.math.uni-wuppertal.de/~klamroth/publications/gopfkl07.pdf),
Definition 1.1, section 2 and Definitions 3.5--3.6/Theorem 3.13, provide a
closer geometric vocabulary: convex sections do not imply connectivity, and
coordinatewise path properties need additional hypotheses. Our source is
biconvex, but that fact alone gives no finite component bound (even an
arbitrary set of distinct diagonal points has singleton, hence convex,
sections). The finite receipt presentation and comparable-cell intersection
are additional structure. The read source does not state this receipt-count
bound; this is a scoped comparison, not an exhaustive novelty conclusion.
