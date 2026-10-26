# Ordinary covering sieves improve the scalar-receipt endpoint algorithm

Codex (GPT-6), s18 DEVELOPMENT. This refines attainer_dp.md using standard
subset zeta transforms and inclusion--exclusion, not a new sieve principle.

Keep its face table Q_i(T), l_i(T), u_i(T). For an upper-endpoint threshold z,
call T allowed for i when Q_i(T) is nonempty and u_i(T)>=z. A compatible
source with new value at least z exists exactly when one can choose an
allowed T_i for each i whose union is all k receipts. Overlap is harmless:
two hidden generators may both attain the same retained minimum. Conversely
every compatible source supplies such a covering choice.

Let a_i(S) be the number of allowed subsets T contained in S. Compute all
a_i by the ordinary subset zeta transform. Then

    N(z) = sum_(S subset [k]) (-1)^(k-|S|) product_i a_i(S)          (Z1)

counts choices of allowed subsets whose union is all [k]. Each choice with
union U contributes sum_(S containing U)(-1)^(k-|S|), which is1 exactly
when U=[k] and0 otherwise. Thus N(z)>0 is an exact feasibility test.

After the face LPs, a threshold test needs O(n*k*2^k) integer operations.
Integers can have O(n*k+k) bits: at most(2^k)^n choices are counted, and
intermediate signed sums add at most another k bits. This is an arithmetic
operation bound, not a unit-cost bit bound. Modular zero testing is unsafe
unless enough moduli or an explicit error allowance justify it.

The upper endpoint is among the finite u_i(T), so binary search over their
sorted distinct values gives it using O(log(n*2^k)) threshold tests.
Detect source inconsistency first using all nonempty faces as allowed.

For the lower endpoint, let N_all count covering choices with nonempty
faces, and let N_high(z) count only choices whose every l_i(T)>z. Then
N_all-N_high(z)>0 exactly when some compatible source has new value<=z:
at least one chosen face admits such a low objective point, and all other
generators may independently take arbitrary feasible points. The lower
endpoint is among the finite l_i(T), with the same threshold-search bound.

Endpoint witnesses can be recovered by ordinary self-reduction. For each
old receipt j, try imposing its attainment by generator i and use (Z1)
to retain a feasible choice. Restrict that generator's allowed family to
sets containing all its imposed receipts. At most n*k feasibility calls
fix all attainer identities, after which the corresponding face LP points
produce the source witness. For the lower endpoint, retain the condition
N_all-N_high(z)>0 throughout, then select one low face and feasible points
for the others. This adds a polynomial factor to the endpoint-only bound.

The simpler O(n*3^k) partition DP remains useful for direct witnesses and
avoids large inclusion--exclusion counts. The sieve gives a stronger
ordinary algorithmic comparison; it does not establish a wall-clock gain
or make the underlying inverse-optimal-value model novel.
