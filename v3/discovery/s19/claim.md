# V19-R/v1: exact scalar ranges from retained optimum receipts

Codex (GPT-6), October26,2026. DEVELOPMENT. First explicit contribution
event for the conditional-receipt direction developed in s18 and s19.
It is distinct from N16-C/v1, O18-M/v1, I13-R/v1 and F01/v1.

## Fixed mathematical claim

Let n>=1 independently uncertain vectors x_i belong to supplied nonempty
compact rational polytopes B_i, in possibly different positive dimensions.
The admitted source is their product intersected with k interval receipts

    a_j <= min_i g_ji(x_i) <= b_j,    a_j<=b_j,

where every g_ji is a supplied rational affine form. A future scalar is
V(x)=min_i f_i(x_i), for supplied rational affine f_i. The same vectors
underlie all receipts and the future readout. Independence is a product
uncertainty-set premise, not an asserted probabilistic independence.

The proposed result is an exact, gap-preserving description of V's entire
attainable set as a union of at most n*2^k closed intervals, or an explicit
inconsistency answer. It uses at most2*n*2^k local rational LP solves and

    O(n*3^k + n*2^k*log(n*2^k)) comparisons,

with O(n*2^k) scalar table storage plus original inputs, backpointers and
local primal/dual witnesses. All LP bit costs, exact-number lengths and
retained input/certificate bytes are additional charged resources. For
every requested attainable rational q, the algorithm reconstructs a
compatible rational source with V=q. The k=0 and n=1 conventions are part
of the claim. The proof is the anchor formula AR1 in anchor_ranges.md.

The result admits an exact rational certificate: for EVERY indexed local
slice supply either a Farkas infeasibility vector or attained minimum and
maximum with matching nonnegative LP dual multipliers. The verifier
rebuilds those constraints from the caller's original problem, checks all
identities and inequalities, and recomputes the anchored interval union.
It never treats an omitted slice as infeasible. Soundness is relative to
the supplied source and receipt premises; it does not authenticate them.

The resource distinction is a fixed-parameter whole-range construction in
the number k of retained receipts, in place of enumerating n^k witness
assignments. It is not a proven lower bound against every ordinary solver,
nor an observed speedup. The output may itself require exponentially many
components: output_size.md gives binom(k,k/2) isolated values with n=2 and
growing local dimension. This explicit-output limitation does not apply
automatically to one-value queries or succinct symbolic outputs.

## One useful consequence

Under the positive-cost, full-dimensional, nonzero-tolerance contract in
robust_gap.md, the exact future set is[21,21.2] union[21.9,22.2]. It rejects
a later report band[21.4,21.6] that its interval hull admits. It also
certifies |1/(V-21.5)|<=10/3, conditional on those premises. This supplies
one concrete model-criticism/numerical-stability duty. The cheaper direct
band-feasibility control and winner/full-source retention must be included
in any economic interpretation. No aggregate saving is required or claimed
by this bounded contribution event.

## The contribution event and exclusions

The event is that rigorous reconstruction supports this exact algorithm,
resource statement, rational-certificate soundness and worked consequence,
AND a close comparison supports a useful, moderately novel guarantee or
synthesis beyond a routine restatement already supplying the same input
contract and whole-range output. Readiness includes proof, checker/interface,
novelty and usefulness uncertainty; it is not conditional on those passing.

Ordinary LP duality, disjunctive programming, inverse optimization, subset
partitioning and exact arithmetic are credited machinery. An ordinary
implementation of this same algorithm ties. A smaller retained-information
comparator establishes only an information-dependent consequence. The
event is neither a general mathematical-uncertainty learner nor a promise
to beat strong ordinary methods on every task.

The faster convolution adapters, sparse forest/cycle result, contractibility,
low-rank exact receipts, withdrawal prices, repair radii, mixed decisions,
probability interpretation and practical benchmarks are separate extensions.
None becomes a prerequisite or a borrowed success metric for V19-R/v1.
