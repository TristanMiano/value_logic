# Importing faster subset convolution into receipt reconstruction

Codex (GPT-6), October26,2026. DEVELOPMENT; separate refinement of AR1.
The executed cubic-subset implementation remains frozen.

## Existing primitive and the application delta

Stoian, *Approximate Min-Sum Subset Convolution*, arXiv2404.11364v3,
section3 Theorem3, gives exact min-max subset convolution in soft-O(2^(3k/2))
time. This is an existing primitive, not a new speedup claimed here. Its
ranked Boolean-convolution and chunk-search idea applies to arbitrary ordered
entries; sorting rational values and replacing them by ranks handles our
finite endpoints and the two infinity sentinels without numerical rounding.

Every prefix, suffix and outside table in anchor_ranges.md is a max-min
subset convolution. Negating the entries turns it into min-max convolution.
Thus O(n) calls to the existing primitive replace the O(n*3^k) split scans.
With the explicit elementary implementation reconstructed below, the whole
range follows after at most2*n*2^k local LPs using

    O(n*k^2*2^(3k/2) + n*2^k*log(n*2^k)) arithmetic/comparison operations,

and O((n+k)*2^k) scalar/integer cells plus LP certificates. Integer arithmetic
inside Boolean convolution uses O(k)-bit counts; rational comparisons still
pay endpoint bit length. The small-k naive kernel may be preferable. This
is an imported algorithmic refinement of the conditional-range reduction,
not a measured runtime gain or a new subset-convolution theorem.

## An explicit tagged implementation

For two arrays f,g on the k-bit masks, sort the2*2^k labelled entries
(value, side, mask). Divide the resulting total order into chunks of size
ceil(sqrt(2^k)). At a chunk boundary, activate exactly the entries in the
prefix, separately for f and g. Compute Boolean subset convolution by the
ordinary ranked zeta transform, multiplication and Mobius inversion.

When a mask S first obtains a nonzero convolution count, some witnessing
pair has an entry in the current chunk. Scan its tagged entries. For a
left entry U subset S evaluate max(f(U),g(S minus U)); for a right entry U
subset S evaluate max(f(S minus U),g(U)). Retain a minimizing split.

The first-positive pair proves that the scan contains a candidate no larger
than its first-prefix bottleneck. More precisely, take a globally optimal
pair and the later of its two sorted positions. Before that position's
chunk no pair can have a strictly smaller bottleneck than the global optimum;
if another optimal pair appears earlier, the first-positive chunk still
contains an optimal pair. Every scanned candidate is an actual pair, so
none undercuts the true minimum. This proves exactness, including ties.

Using entry-prefix activation rather than value-threshold activation avoids
silently activating tied entries outside the chunk. Keeping side tags avoids
treating a right-array entry as if it were a left-array entry. Both are
explicit implementation details in this reconstruction; the displayed
untagged formula in the source is not copied verbatim into executable code.
We do not infer that the published theorem is false from that shorthand.

Each mask is scanned once, each scan visits at most one chunk, and there
are O(2^(k/2)) Boolean convolutions. A ranked convolution costs O(k^2*2^k)
integer operations and O(k*2^k) workspace. Intermediate signed integers have
O(k) bits for Boolean inputs. The stored split recovers a witness, so the
prefix/suffix source reconstruction in AR1 retains its original meaning.

## Status

The mathematical import is a stronger ordinary comparator and a possible
implementation improvement. It does not settle whether AR1's full-range
reduction is moderately novel. A finite kernel check should stress equal
values, asymmetry between arrays, unavailable slices and recovered splits.

The [prospectively hashed check](fast_subset_plan.json) subsequently passed:
6,721 kernel cases, including all6,561 ternary array pairs on two-bit masks;
31,344 exact value and split checks;180 previously exposed polygon cases
and472 recovered source witnesses. [Result](fast_subset_result.json).
The implementation makes36,574 Boolean calls and178,408 tagged-entry scans
across the complete panel. These are not comparable units to naive split
counts, and the1,889,706,400ns run is not a controlled speed comparison.
The kernel and probe are now frozen at their recorded hashes. No failures
occurred in this execution. Mathematical novelty remains unresolved.
