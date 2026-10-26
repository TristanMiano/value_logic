# An exact retained summary for majority-closed sources

Codex (GPT-6), s18 DEVELOPMENT. Uses the contact/projection theorem from
closure_receipts.md and fallible_contacts.md. Ordinary2-CNF projection
representations and counting are the direct controls. Novelty is unassessed.

Let unknown nonempty F subset{0,1}^d be closed under coordinatewise majority.
There are reliable retained actions B and nonempty uncertain contact sets
T_i. At most r contacts can be false. For each unary or binary coordinate
set J and pattern a in{0,1}^J retain

    b[J,a] = whether some retained action has that projection;
    n[J,a] = number of reports whose every point has projection a.

The guaranteed feasible-action set is exactly the ordinary2-CNF relation
that forbids every pattern with b[J,a]=false and n[J,a]<=r. Consequently
one can discard the individual report regions after these counts have been
correctly computed, if the only future duty is to answer action membership
or find an action under the same source and reports. Nonempty subcube contacts
contribute only patterns on their fixed coordinates. A contact fixing k bits
updates O(k^2) counters; a target needs O(d^2) pattern tests, and a concrete
action can be found with an ordinary linear-time2-SAT algorithm on O(d^2)
clauses. Source authentication and the closure/error-budget warrants are
separate duties.

For all future budgets0<=r<=R, store counts clipped at R+1. This uses
O(d^2 log(R+2)) bits plus the reliable-pattern flags. With a single fixed r
and no further updates, only the thresholded pattern flags are needed,
using O(d^2) bits. Insertion can use clipped counters; arbitrary later report
deletion is not supported by saturation unless further counts/provenance
are retained. Do not claim that an aggregate proves where its inputs came
from or permits free retraction.

## A matching information lower bound for changing budgets

Fix B to contain the all-one vector and each vector with exactly one zero.
It already supplies every unary pattern and every binary pattern except00.
For each pair e={i,j}, independently choose a count c_e in{0,...,R+1} and
include c_e contacts fixing just x_i=x_j=0. These reports do not force any
other pair's00 pattern. Add R+1 contacts containing only the all-one vector
to ensure the total report count exceeds every allowed r; these add no00.
The full Boolean cube is always a compatible true source.

For a target z_e with exactly zeros i,j, the projection criterion reduces to

    z_e is guaranteed feasible at budget r iff c_e>r.       (P2)

The answers for r=0,...,R recover every c_e. Therefore any deterministic
exact summary answering all targets and all those budgets must distinguish
(R+2)^(binom(d,2)) different report states. It needs at least
binom(d,2)log2(R+2) bits in the worst case. This is a query-information
lower bound, excluding the common fixed B, not a lower bound for one action
or one fixed budget. The upper and lower bounds match in order.

The example also supplies the fixed-budget Omega(d^2) lower bound by using
c_e either0 or r+1. It does not charge the input reports as zero-cost or
claim that counting beats an ordinary2-CNF representation.

## Decision and audit consequences

Changing the warranted fault budget can change the admissible action without
re-reading all reports. The summary answers that particular information
question exactly. It does not estimate the true fault rate. If an additional
audit proves one contact reliable, each pattern forced by that contact can
be marked reliable rather than merely counted. This can authorize an action
whose rare patterns previously lacked r+1 support. A proof of contact truth
must itself be paid for and checked; repeated identical model predictions do
not constitute such an audit.

Selecting audits to cover a target's remaining patterns is an ordinary
set-cover problem when all audit outcomes are assumed positive and their
verified consequences are known. With uncertain outcomes it is an adaptive
information-acquisition problem; the offline cover does not solve it. The
useful object here is the compact exact decision interface and its retention
limit, not a claim of a new optimal audit scheduler.
