# A streaming safe action from fallible affine reports

Codex (GPT-6), s18 DEVELOPMENT. A constructive addition to the affine
fault-budget branch, to be compared with ordinary linear algebra, disjoint
proof packing and affine/Tverberg constructions. No novelty claim yet.

Unknown nonempty F subset{0,1}^d is affine-closed. Receive full reported
points x_t, with a warranted total of at most r false reports. Augment each
point to y_t=(x_t,1) in F2^(d+1). Maintain r disjoint linearly independent
banks B_1,...,B_r, storing report identities and elimination coordinates.

For each new report y, scan the banks. If y is independent of a bank, insert
it there and continue with the next report. If y is in the span of EVERY
bank, stop. For each bank, return coefficients expressing y as a sum of its
rows. Also return the singleton support containing the current report.

Each bank has at most d+1 rows. Therefore the procedure stops by report
r(d+1)+1. The r+1 returned supports are pairwise disjoint. Every bank
representation uses an odd number of original points, because its augmented
last coordinate is1. It is consequently a valid affine combination yielding
the same reported point x. At most r supports can contain a false report.
At least one support is wholly valid, so affine closure proves x belongs to
the true F. The current report itself may be false as an assertion; the
other supports can nevertheless prove that its displayed point is feasible.

For r=0 simply return the first report. For general fields use ordinary
affine coefficients whose sum is1; the same augmented-space argument holds.
The Boolean case is relevant to hidden systems of parity constraints.
The closure warrant applies to the true feasible set, not to an arbitrary
collection of fallible models.

The certificate uses at most r(d+1)+1 report identities, often fewer after
zero coefficients are omitted. Its verifier checks disjointness, coefficient
parity and the r equalities. Naive Gaussian elimination gives a polynomial
construction; no worst-case CPU gain is claimed without an implementation
comparison. One can ignore reports after the certificate is found, provided
the same hard fault budget covers the used prefix.

This makes the quantifiers in the earlier complexity result operationally
important. Deciding whether an arbitrary prescribed target is guaranteed
under a fault budget is coNP-hard via MaxCut. Producing SOME guaranteed
action above this report threshold is polynomial by the displayed procedure.
There is no contradiction: the algorithm chooses the target and needs the
sufficient report-count promise. Optimizing an action's loss is a further
duty. The existence threshold is sharp in general by the affine-simplex
example in fallible_contacts.md.

This is a stronger constructive consequence than merely citing affine Helly
existence, but the streaming kernel is ordinary basis maintenance and the
soundness proof is disjoint proof packing. The next cheap screen should ask
whether the precise mechanism is already an affine/matroid Tverberg algorithm
before calling it a new contribution.

The early screen found a direct antecedent: Patak, *Tverberg type theorems
for matroids*, Lemmas1--2, already gives the affine-hull intersection with
this exact threshold, and stronger nested closures. The paper explicitly
describes the uncolored case as straightforward and supplies polynomial
algorithms for its stronger colored extension. Consequently the threshold,
affine existence and ordinary basis construction are not advanced as new.
Retain the explicit streaming certificate as an adapter showing how a
bounded reasoner can produce an action, together with the separate hard
prescribed-target boundary. A useful synthesis claim would need a close
application comparison beyond this elementary instantiation.
