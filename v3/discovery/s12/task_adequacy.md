# A fallible model can be wrong globally and still warrant every permitted task

Codex (GPT-6), October 19, 2026. DEVELOPMENT, connecting Q1–5.
This uses ordinary propositional forgetting/projection. The proposed adapter
specifies exactly which weaker source event survives the permitted receipts.

## Fixed observation and target interfaces

Let F be a nonempty Boolean source on n original coordinates. Let Q be the
coordinates that the interface may observe, and let J range over a nonempty
declared family of target-clause scopes. Define the enlarged source

    H = {x: for every J, x_(Q union J) belongs to P_(Q union J)(F)}.

Projection here is existential: each J can have a different F-world witness.
H contains F, and can contain worlds that violate F. For every receipt h on
any subset of Q, including ones reached adaptively, and every declared J,

    P_J(H AND h) = P_J(F AND h).

Proof: one inclusion follows from F subset H. For the other, take x in H AND h.
Its J-witness w in F agrees with x on all Q union J, hence satisfies h and
has the same J-pattern. Empty branches agree too: any one witness shows that
a Q-receipt compatible with H is compatible with F.

Thus the local permission compiler returns exactly the same masks for F and
H after every permitted receipt. Any mask certified over F AND h also works
on every actual world in H AND h. A conjunction of target clauses is safe
clause by clause; no single F-world shared by all J-witnesses is needed.
Unary maps whose target coordinates depend only on the original same-scope
bits have the same conclusion. With copies, pull the scopes and observations
back to their original coordinates first; dynamically introducing new origins
can enlarge the required interface and strengthen H.

H is the largest source with these conditional projections. If some source
W has the same projections for every Q-receipt and every J, take x in W and
use the complete receipt x_Q. Equality supplies an F-world agreeing on Q and J,
so x belongs to H. This maximality concerns the declared projection service;
one fixed target or a restricted set of masks may need still less information.

There is also an operational converse for the universal menu of one-clause
targets on declared scopes and arbitrary toggle masks. If x lies outside H,
some full Q-receipt leaves its actual J-pattern absent from F. Choose a mask
that maps that pattern to the clause's falsifying pattern. Every retained
F-pattern satisfies the clause after the mask, while actual x violates it.
If the receipt itself contradicts F, the interface must flag that conflict;
the converse then witnesses a failed source-compatibility service rather than
a legitimately released action. Never use an empty source as permission.

## Why target projection alone is insufficient

Let F be q implies a, Q={q}, and J={a}. Its initial projection on a is full,
so every actual a is initially locally compatible. If actual q=1,a=0, the
receipt q=1 makes F force a=1. A compiler can now certify toggling a to achieve
NOT a, but that toggle makes actual a one. Including Q in the projected
adequacy condition prevents this mistake. The required envelope is q=>a.

In contrast, let F=(q=>z) AND (z=>a), with the same Q and J. The envelope is
again q=>a and forgets z. Actual (q,z,a)=(1,0,1) violates F but belongs to H.
After observing q=1, toggling a to achieve NOT a works in the actual world,
despite the false intermediate model claim about z. This is a useful scoped
reliance on a wrong model, with an exact sufficient premise.

## Binary preparation and what gets paid

If F is 2-CNF-definable, every projection onto Q union J is 2-CNF-definable.
Take its entailed units and binary clauses, or compute the relevant implication
reachability facts. Their conjunction over J represents H exactly. With q=|Q|,
t=|union J| and m bounded-width target scopes, the number of candidate binary
relations is O(q^2+q*t+sum_J |J|^2), rather than requiring all n-coordinate
facts. This is a representation-size bound, not a free compilation algorithm.
One may pay ordinary 2-SAT entailment tests for those relations; initial model
creation, proofs and physical observations remain separate costs.

The general source can require exponentially large projections. Large Q can
eliminate the expected savings. Dropping clauses that merely look syntactically
irrelevant is unsound: hidden z in the example transmits q=>a, which must remain.

## Fallibility and calibration contract

A justified bound Pr(actual x not in H)<=epsilon gives one unconditional
failure bound for all adaptive receipts and certified actions within the fixed
interface. It can be strictly smaller than Pr(x not in F), even when that latter
probability is one. No new epsilon is spent for every edit on the same original
world. Conditional error among released cases need not be at most epsilon.

Checking H on calibration examples can require only Q union union J labels,
instead of labeling every original model coordinate. This is a possible audit
scope saving, not a measured fee reduction. Direct calibration of the deployed
task or an ordinary forgetting-based controller is a strong comparator and
must receive the same labels. H must be fixed before a simple calibration
bound is applied; adaptive selection among envelopes needs simultaneous,
held-out or other justified selection-aware evidence.

For a real instance, verifying H by learning every target coordinate may cost
more than the action it was meant to support. The constructive gain is the
weaker adequacy event and exact transport through permitted observations;
an economical way to justify that event is still an application duty.

## Prior and disposition

Lin and Reiter, Forget It! (1994), Definition 1, Propositions 2–3 and Theorem 4,
already give the model projection and preservation of unforgotten consequences.
The present envelope intersects several such projections and specifies the
observation/operation contract. It does not invent forgetting or establish that
ordinary logic requires every model detail to be true. Retain as a small
synthesis with an explicit counterexample and a prospective finite check;
priority and complete-cost usefulness remain unassessed.

The [finite screen](task_adequacy_probe.json) passes 4,050 conditional-projection
comparisons on 150 sources, including 75 binary-source reconstructions. The
envelope admits 713 extra worlds across 62 of those sources. Outside it, the
screen finds 924 contradictory full receipts and 1,249 concrete unsafe-action
witnesses; these are separate failure modes. Runtime is 0.0354187 seconds.
No empirical model-coverage or calibration-fee claim follows from these counts.

## A narrower fixed-policy variant

The full Q-interface can be unnecessarily demanding if a supplied finite
observation tree T never buys all Q-coordinates on one path. For each leaf h,
let J_h be its allowed target scopes. Define H_T by taking the union, over
leaves, of the worlds satisfying h and every constraint
x_J in P_J(F AND h) for J in J_h. A leaf with F AND h empty is excluded.
Leaves are disjoint because T is a deterministic observation tree.

For every x in H_T, the actually reached leaf has exactly the same local
projection warrants as F at that leaf. Consequently every allowed mask at
that leaf is valid at actual x. H_T is the largest envelope preserving those
leaf projection services: the proof is the same one-leaf witness argument.
It can be strictly larger than the all-Q envelope because observations that
occur on different branches need never be combined. The tree, observation
semantics and leaf interfaces must be fixed for this event to remain valid.
A random tree may be conditioned on its independent public random tape, or
requires a specified joint adequacy event; it does not inherit one fixed
tree's calibration for free.

This variant has a possible exponential tree cost and does not justify
changing the controller after inspecting calibration labels. It is retained
as a semantic option, without a new learner or a large test suite.

There is a useful monotonic tradeoff: enlarging Q or adding target scopes
shrinks H, while weakening F enlarges H. More operational freedom can demand
a stronger model-adequacy event; weaker model reliance can reduce the safe
action menu. A policy-restricted envelope can avoid paying for hypothetical
queries the controller will never make. These are exact set inclusions, not
an asserted empirical benefit from deliberately withholding observations.
