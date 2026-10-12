# Paid sources for the acquisition planners

ChatGPT (GPT-6 Astra Pro), October 12, 2026 UTC. DEVELOPMENT; constructive
workload design, not an executed comparison. Delegated work contributes no
additional principal research time. Parent: [s04 session](session.md).

## The interface correction comes before a benchmark

A useful source is a fixed family of mathematical claims indexed by a context
`i` and a revision-tree vertex `v`. Let `X_v(i)` be the claim's Boolean sign.
The cohort and revisions are public; labels appear only through paid checked
evaluation. Uniformly sampled cohort identities support inference about fixed
mathematical counts. They do not turn a proposition's truth into an intrinsic
random variable.

An edge parity is `E_(u,v)(i)=X_u(i)*X_v(i)`. The fixed forecast that a revision
preserves its parent's result is simply `s_e=+1`. Producing that sign is cheap;
its accuracy is initially unknown. Calibration must acquire both endpoint
labels or a genuine relational proof. A base result is also paid unless a
particular source construction proves it publicly.

This exposes a mismatch with a black-box edge-query model: executing one
vertex can help several adjacent edge audits, and gives its own label to every
method. Charging independent full endpoint evaluations per edge would hide
real reuse. Conversely, giving a parity receipt the price of one endpoint
would omit work. The public observation interface must therefore expose
vertex receipts and any separately supported relational proofs. A matched
controller may use everything the observation actually reveals.

If a requested parity reduces algebraically to a product over a boundary
vertex set `B`, its direct acquisition bill is the union of missing vertex
receipts, plus checked algebra and registry work. It is not the sum of the
costs of evaluating every edge in its original expression. Acquisition costs
are set dependent, and realized solver costs can depend on the labels. The
new forest/boundary construction should use this interface rather than
pretend that the earlier additive edge-price model already covers it.

## Branch A: satisfiability under a public revision tree

**Source.** A finite cohort of CNFs, generated without solving, and a small
revision tree of syntactically specified clause additions, deletions and
replacements. A row uses the same base formula across all revisions. The claim
at a vertex is satisfiability of that revision. Use both restrictive and
relaxing edits so the task is not entirely discharged by one monotonic rule.
Neither edit positions nor formula identities are selected using truth.

**Already available evaluator.**
[p308_cnf.py](../../experiments/p308_cnf.py) provides `make_query`,
`checked_purchase`, and source-bound receipts. Its DPLL implementation is
pure Python; SAT witnesses receive a separate clause check, and UNSAT uses
either a checked simple contradiction or independent assignment enumeration.
The unchanged finite service admits at most 12 variables, 64 clauses and
width four. It is a transparent development interface, not a modern SAT
performance benchmark. The larger prior SAT workloads used a native dependency
that is absent in this environment; their old evidence stays unchanged.

**Accessible prediction and evidence.** The constant no-change forecast is
available immediately. An optional frozen syntactic forecast may use the
public formula/edit and must pay its actual feature computation. Checked SAT
witnesses may be tested against other revisions. UNSAT of a formula transports
to a verified clause superset, and SAT transports to a verified subset; the
identity/subset or witness checks are paid and available to all arms. No
untested source-frequency, independence claim or evaluator label is advice.

**Concrete purpose.** A consumer changes the stakes attached to correct answers
about several proposed constraint revisions, or changes its price of exact
evaluation. A prepared calibration source may support many such fixed query
plans. A smaller direct policy bank may instead acquire only the contrasts
needed for the actual requests. Both routes must pay for their calibration
and deployment computation; long hypothetical repetition cannot make the
initial acquisition bill disappear from a reported comparison.

**Strong controls.** Include exact DPLL with a common receipt cache and
witness/monotonic transport; direct evaluation of a small fixed policy bank;
and direct boundary-moment acquisition after the same algebraic cancellation.
A conventional method receives the candidate's valid confidence bounds and
can run the identical profile optimizer. The possible contribution is a useful
integration or source-specific saving, not superiority over that whole class.

**Why try it first.** The mathematical meaning, proof checks and an explicit
operation tariff already exist. It replaces supplied edge probabilities with
actual paid evidence without writing a new solver. The obvious difficulty is
also informative: the strongest exact/transport control may settle most small
instances so cheaply that statistical preparation never pays.

## Branch B: graph revisions and certified route thresholds

**Source.** Fixed nonnegative integer weighted graphs, source/target vertices,
and a revision tree that removes, restores or changes specified edge weights.
At a vertex ask whether the shortest route is within a public threshold.
Graph generation and thresholds must be fixed without examining shortest-path
answers. This represents consequences of proposed network changes directly.

**Prediction and ground truth.** Forecast no threshold-status change after a
small edit, or use a paid bounded search fixed before calibration. An exact
search obtains distance and a route. A route with length below the threshold
checks a positive claim. A potential `p` satisfying `p(s)=0` and
`p(v)<=p(u)+w(u,v)` for every directed edge bounds every source-to-target path
from below; `p(t)` above the threshold checks a negative claim. This follows
by summing the edge inequalities along any path. Certificate construction,
edge scans, integer arithmetic and storage are all paid. Unreachable cases
need their own checked reachable-set certificate.

**Sharing and controls.** A retained route can survive several edits; a
potential must be rechecked only under a justified dependency rule. Direct
shared exact search and certificate maintenance are essential controls, along
with direct policy-contrast sampling. Different thresholds for the same
unchanged graph must reuse a known exact distance instead of repeating a
statistical audit. For value semantics, retaining certified distance intervals
may be more useful than reducing everything to Boolean threshold outcomes.

**Opportunity and first screen.** This branch has a meaningful revision
interpretation and independently checkable answers. It needs a new small
evaluator and receipt layer. Before substantial experiments, ask whether a
single exact run already answers the proposed request stream; if so, change
the substantive use case rather than artificially taxing that control.

## Branch C: precision-limited mathematical evaluation under edits

**Source.** Integer-coefficient polynomial expressions evaluated at rational
inputs, with explicit coefficient or expression revisions. The proposition
is a specified sign/threshold comparison. The context supplies coefficients
and input, not the exact sign. A bounded floating or interval evaluator is a
fallible proposal; exact rational arithmetic or outward-rounded bounds can
deliver checked labels. Large intermediate arithmetic creates real evaluation
work, rather than an artificial delay attached to a precomputed bit.

**Evidence and sharing.** Charge proposal evaluation and exact/interval work,
record operand sizes, and retain common powers or subexpressions with their
identities. A verified interval avoiding the threshold is an exact receipt and
needs no statistical calibration. Only unresolved fixed proposals require
source-level error bounds. Formula shape and input ranges are specified before
labels; do not create only cancellation cases where a preferred method wins.

**Controls.** Adaptive-precision interval evaluation, common-subexpression
reuse and direct paired evaluation are strong ordinary alternatives. A
per-comparison confidence interval can be too expensive if errors are rare:
statistical evidence that a proposal is very reliable can require far more
exact evaluations than the request stream needs. That cost consequence should
guide new constructions, rather than postponing it to a large adversarial run.

## Minimal implementable next step

Use Branch A as the first real-source adapter and keep B/C open. The adapter
can be small; it does not need a new research framework:

1. `source(row_id, vertex)` returns the immutable CNF identity and public edit.
   A root solve is an ordinary paid request. No hidden truth table is built
   during generation or exposed through the policy API.
2. `acquire(row_id, vertices, cache, cap)` returns successful receipts and
   unresolved failures. It deduplicates endpoints, tries valid retained proof
   transport, then calls the existing checked solver on remaining claims.
   Record the charged provider operations and wall time separately. New adapter
   scans, transport checks, forecast work and bookkeeping must also appear in
   the full bill; the old provider tariff does not automatically price them.
3. `observe_feature(row_id, B)` requests only missing boundary vertices,
   multiplies successful signs, and returns unresolved if any required label
   is missing. A sampled row stays in its original sampling stream even when
   that feature is unfinished. Cheaply completed rows cannot replace it.
4. Share the same accumulated receipt pool between marginal and direct-contrast
   statistical calculations when comparing information use. For performance
   comparisons, each method starts from the same permitted state and pays its
   own acquisitions; a diagnostic oracle's labels are inaccessible.
5. Begin with a tiny semantic/cost adapter check on both SAT and UNSAT examples,
   including an edit whose retained witness fails, a transport hit and an
   unresolved capped purchase. Only then prospectively choose an untuned mixed
   cohort and modest request stream. Do not select the source scale or number
   of repetitions to manufacture a break-even result.

The comparison to resolve is narrow and useful: when actual labels are paid
for, does broad marginal calibration enable enough later decisions to cover
its acquisition cost, or do sparse shared contrasts need less evidence and
less conservatism? The development can discover a hybrid that acquires a small
reusable feature core and fills in only the missing boundaries of later
requests. No source accuracy, economic advantage or confirmation readiness is
claimed by this design document.
