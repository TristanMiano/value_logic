# S08T: transport one aggregate confidence event through value/source changes

Codex (GPT-6), October 11, 2026. DEVELOPMENT. No novelty or readiness claim.
Lineage: S01/S04/S05/S07/S08, ordinary confidence-region propagation and
cardinality-constrained linear optimization.

## 1. Separate a source confidence event from later value queries

Let fixed deterministic base bits be y=(y_1,...,y_N). A sound sampling service
provides a simultaneous confidence set C_t for that same y, with

    P[y belongs to C_t for every t] >= 1-alpha.

On this one event, every function can be bounded over C_t. The user may choose
later value weights after observing earlier output: if bounds really optimize
over all of C_t, this adaptivity does not need another alpha allocation for
each weight vector. This is ordinary confidence-set propagation, not a
license to apply separate fixed-level tests repeatedly to new targets.

Likewise, if a checked relation T_t connects the base y to an edited y^t,
optimize the new value over all pairs admitted by C and T_t. Relations and
weights may change adaptively if their soundness holds pointwise for the actual
base/edited objects. The same original confidence event implies simultaneous
validity of every such transported bound, for arbitrarily many later queries.
Unverified model proposals may enlarge the relation or schedule checks; they
must not silently remove possible pairs. The relation carries semantics, not
the statistical sampling procedure.

If instead an edit is selected using sampled outcomes and one simply reuses
those sampled indices as though they were a fresh uniform sample of the new
target, the old test does not supply this guarantee. Use pointwise transport,
a common simultaneous confidence source, or a new independent sampling lottery
with a declared risk budget. A frozen bound on one count is not automatically
a simultaneous collection of separately tested count thresholds.

## 2. Closed forms for changed task probabilities and local edits

Suppose the confidence source says only L<=sum_i y_i<=U, and task probabilities
q_i>=0 sum to one. The sharp lower/upper bounds on sum_i q_i y_i are the sum
of the L smallest and U largest q_i, respectively. Existing positive/negative
receipts further restrict which coordinates may be chosen. A mean under
uniform task selection is not automatically a mean under a changed law q.

For an arbitrary edit confined to indices A, let B be its complement. The
sharp bounds using only this support information are

    lower = sum of the max(0,L-|A|) smallest weights in B;
    upper = sum_(i in A) q_i + sum of the min(U,|B|) largest weights in B.

The lower construction spends as many required base ones as possible inside
A and lets the edit erase them. The upper construction sets every edited
coordinate to one, placing available base ones on the largest weights outside.
Under uniform q these reduce to max(0,L-|A|)/N and min(N,U+|A|)/N.

For monotone increases y^t>=y (e.g. clause removal), the unedited lower bound
also survives. For monotone decreases (clause addition), the unedited upper
bound survives. These improve one endpoint without identifying the changed
truth values. Duplicate edits and reversions must be compared with the fixed
base version: count currently possibly different coordinates, not the sum
of every historical edit's support size.

## 3. A more general exact O(N log N) kernel

For each i admit a nonempty set S_i subset {(0,0),(0,1),(1,0),(1,1)} of
base/edited pairs. Unchanged coordinates allow {(0,0),(1,1)}; additions allow
{(0,0),(1,0),(1,1)}; removals allow {(0,0),(0,1),(1,1)}. Accepted old/new
receipts intersect these sets with the appropriate coordinate equality.
The actual pair must remain admitted. Let edited value be c+sum_i w_i*y_i^t,
allowing signed rational weights for utility contrasts.

For the lower bound, for each base bit x define

    f_i(x) = min {w_i*z : (x,z) in S_i}.

An unavailable x is forbidden. Coordinates allowing only one base bit are
forced; subtract their one count from [L,U] and add their f_i cost. For each
remaining coordinate both base bits are allowed. Add f_i(0) to the baseline
and form delta_i=f_i(1)-f_i(0). The remaining problem is to choose a subset
of these deltas with cardinality in the adjusted interval [l,u]. Sort them
ascending. For any cardinality k, its first k elements minimize the sum.
Choose k equal to the number of negative deltas, clipped to [l,u]; zeros may
be chosen or omitted to satisfy the interval. Add the selected deltas.

For the upper bound replace min by max, sort deltas descending and choose
the number of positive deltas clipped to [l,u]. This is the ordinary greedy
solution to a cardinality-constrained separable problem. Sorting costs
O(N log N) comparisons; exact rational arithmetic has a separate bit cost.
Store the selected base bits and the minimizing/maximizing edited bit for
each coordinate to reconstruct endpoint witnesses. No exponential enumeration
of all base/edited worlds is needed for this stated product-relation source.

This does not optimize an arbitrary coupled CNF relation. Dropping coupling
gives an outer bound that may be loose; importing independence as a truth
assumption would be invalid. The product relation is a representation choice,
not a claim that mathematical answers are independent random variables.

## 4. Inconsistency and post-selection boundaries

If an S_i is empty or the adjusted count range has no feasible cardinality,
return a source/evidence conflict. Do not exploit an empty confidence source
to warrant every action. It may indicate a stale identity, a bad relation or
the confidence event's permitted statistical failure. Resolve the source or
use a separately specified fallback; the artifact must preserve the conflict.

The direct one-sided tests in the earlier prototypes use a fixed threshold
selected before sampling. Their output warrants that threshold only. A full
count confidence set can support post-hoc thresholds, but repeatedly querying
the direct tests at newly chosen thresholds without another argument is not
equivalent. Similarly, if more proofs outside a sampled group increase an
offset b after the lottery begins, a full confidence set for the unchanged
group can combine with those proofs pointwise. The fixed-boundary test should
not silently replace its null at each new offset.

## 5. Next constructive evidence

Implement the sorted kernel with exact rational endpoint witnesses and check
small product relations against enumeration. Then construct a versioned value
service that binds a frozen base confidence count to explicit local edits and
changed task weights. A small real SAT stream can test whether transported
warrants avoid repeated solver work; prior proof/sampling/setup costs and the
ordinary identical-kernel comparison must remain explicit. This is a new
developmental integration, not an 80%-ready material claim.

## 6. Initial kernel outcome

[transport01.json](transport01.json) matched exact endpoints on 350 seeded
cases at N<=6, enumerating 7,712 pair worlds, including 23 infeasible count/
relation sources. It also matched 256 arbitrary-local-edit closed forms and
two explicit conflict cases. Endpoint witnesses are constructed and checked.
One prepared-input run took 10.3468 ms at N=1,000 and 110.958 ms at N=10,000
for both bounds with exact rational arithmetic. These measurements include
endpoint construction and local feasibility checks, but exclude common input
generation and output serialization. A complete service must also pay for
source binding, relation construction and updates. Cheap uniform-weight
support formulas are mandatory ordinary special-case comparisons.
