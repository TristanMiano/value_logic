# P3-01: imprecise probability trees and the local-model boundary

Contributor: **ChatGPT (GPT-6 Astra Pro)**, principal researcher.
Date: October 7, 2026 UTC. This upgrades source S09 from its earlier
abstract-only lead. It is selected primary reconstruction, not a complete
proof audit or a new learning/recursion theorem.

## 1. Version and exact reading contract

Gert de Cooman and Filip Hermans,
[*Imprecise probability trees: Bridging two theories of imprecise probability*](https://arxiv.org/pdf/0801.1196v1),
arXiv:0801.1196v1, January 8, 2008, 30 pages. Printed page numbers are used.

| Locator | Selected interface and import boundary |
|---|---|
| §§2.1–2.3, pp.2–7 | Bounded-depth event tree, potentially infinite branching; Reality's available moves do not depend on Sceptic's moves. Coherent protocol has conic Sceptic move spaces and linear gain maps. |
| §3.1, D1–D4; §3.2, equations (4)–(5), Proposition 2, pp.8–9 | Accepted-gamble coherence; contingent conditional lower/upper prices on nonempty events. Proposition 2.7 gives an inequality under its partition-conglomerability and well-definedness assumptions. |
| §4.1–4.3, D5', Theorem 3, pp.11–13 | Local conditional assessments specified at the root; natural extension and cut consistency. These are not arbitrary dynamically learned future beliefs. |
| §4.4–4.5, Theorems 6–7, pp.14–15 | Game/assessment correspondence and concatenation for the constructed local-model extension. |
| §8 and concluding discussion, pp.20–23 | Backward inference and scope of local-model computation; no generic finite-runtime theorem imported. |

The conditional-price definition is not division by an event probability.
It therefore supplies an established comparison beyond ordinary positive-mass
conditioning, with its own nonempty-event and behavioral assumptions. No rule
for an empty mathematical contradiction is imported. No weak-law, arbitrary
learning, whole-construction or full counterpossible theorem is imported.

## 2. Consequences for the phase-three comparison

The source connects numerical lower/upper expectations, sequential prediction
and game-like prices. Those broad ideas cannot be a distinctive phase-three
claim by themselves. Its selected correspondence also has structural
assumptions: scaling a feasible move by any positive factor stays feasible,
and the gain map is linear. A physical computation policy with a hard budget
need not form such a cone. For example, the permitted scalar moves `[-1,1]`
contain one but not twice one. One cannot import the conic protocol theorem
for that constrained policy solely by naming its costs prices.

This does not prevent a bounded controller from using an imprecise uncertainty
model. It says that the controller's feasible computation policies and the
belief model's acceptable gambles are different mathematical objects unless
an explicit bridge relates them. Cost and access limits still need their own
analysis under P3-07's contract.

The local assessments are also explicitly conditional assessments held at the
initial node, not whatever a future adaptive forecaster may later output.
A learning or revision algorithm must establish its relation to that source
model. Coherence of a static tree alone does not train it. Similarly, bounded
tree depth is not finite executable cost when a level can have infinitely many
children or a local lower-expectation query is itself expensive.

## 3. A richer shared model need not obey the same recursion

Our separate finite reconstruction uses Boolean `X,Y` and these two joint laws:

| Law | `00` | `01` | `10` | `11` |
|---|---:|---:|---:|---:|
| `P` | `1/2` | `0` | `0` | `1/2` |
| `Q` | `0` | `1/2` | `1/2` | `0` |

Let the admissible global family be their convex hull, with a **single shared**
mixture parameter `theta`: `R_theta=theta P+(1-theta)Q`, `0<=theta<=1`.
Every law has fair `X` and fair `Y`. For task cost `f(X,Y)=Y`, its global
lower and upper expected costs are therefore both `1/2`.

Conditional on `X=0`, the probability of `Y=1` is `1-theta`; conditional on
`X=1`, it is `theta`. Taking each conditional lower envelope separately gives
zero on both branches, and taking each upper envelope gives one on both.
Iterating these branchwise lower/upper envelopes from the fair root yields
zero and one, not the global value `1/2`.

The shared relation has been discarded: the two conditional probabilities
must add to one. Allowing an independent local choice on each branch admits
the law `Y=1` always (and the law `Y=0` always), neither of which is in the
original convex hull. Such local extension can be a valid larger uncertainty
model; it is not exact preservation of the supplied global family.

With an available fallback of cost `3/4`, minimizing worst-case expected loss
at the root over the original global family prefers the `Y`-cost action at
`1/2`. The same root criterion over the larger local family uses the fallback,
since its upper `Y` cost is one. The decision consequence comes from changing
the admitted dependence information, not from changing the notation for the
same expectation. This is an ex ante action/commitment service: a fresh
conditional choice after observing `X`, or a different criterion such as
minimax regret, need not agree. The [independent same-model review](imprecise_tree_review.md)
reconstructs those qualifications.

There is no counterexample to the source's Theorem 7 here. That theorem uses
the natural extension built from the stated local assessments. The richer
global family in this example adds a cross-branch coupling which those local
envelopes alone do not retain. The source itself distinguishes Proposition
2.7's conditional inequality from its particular concatenation equality.
Our finite comparison is direct arithmetic and does not require importing
the general inequality's proof.

This is an elementary two-law separator, not a new theorem about arbitrary
credal sets or the P3-02 characterization. It identifies a future proof
obligation: a recursive cost interface must preserve the shared uncertainty
it claims to retain, or declare the larger family and its conservative loss.

## 4. Verification and resources

The principal inspected the version-pinned PDF and selected definitions and
statements directly. PDF extraction makes lower and upper bars hard to
distinguish in some text; the source's equation numbers, conjugacy and explicit
lower/upper descriptions control the reading. No full appendices, statistical
weak-law proof, numerical learner or final evaluation were executed.

The finite table and its conditional probabilities were reconstructed by hand;
they are not included in the earlier `finite_checks_1.json`. Source reading
and derivation receive only their observed principal L/D segments. No agent
resource span is added to the principal clock, and no new source-index entry
is created for the already existing S09 identifier.
