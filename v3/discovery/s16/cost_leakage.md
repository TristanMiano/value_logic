# A verification invoice can disclose the hidden check

Codex (GPT-6), October24,2026 UTC. DEVELOPMENT; pass49.
This connects the checking construction to the original question about
information carried by computation costs. It is a mathematical interface
attack, not an attempted exploit of any service or machine.

The sealed-checker theorems require that the proposer observes only the
allowed Boolean response and independent public repairs. A correct result
does not imply that its execution cost is independent of the private input.

Let A(x)=0 on a q=2^b point field/grid, and use one hidden uniformly random
test point a. Permit semantically constant-zero programs whose charged
operation count is1 or2 according to bit j of their input's public encoding.
Every such program is globally correct and ALWAYS accepted. If its exact
invoice is released, b correct proposals recover all bits of a. The next
proposal B(x)=x-a is a nonzero degree-one polynomial that agrees at the
hidden point and is therefore falsely accepted with probability1.
For a fixed independent false polynomial the original bound was1/q.
There has been no earlier false proposal or public correction to consume
a rank/mistake budget. This explicitly breaks that bound if cost disclosure
is added to the interface. Semantic degree0 did not restrict control-flow
cost in the constant programs.

With several private points, invoice queries that count whether a point
equals each public grid element can recover the sample multiset. A polynomial
vanishing on it then defeats checking when its number of distinct roots
fits the admitted degree bound. This qualification matters: more than D
distinct points already determine a degree<=D identity, with no secrecy.

## A finite leakage allowance repairs the union bound

Suppose that, after conditioning on independent public randomness, the
ENTIRE extra disclosure transcript has at most J possible values, and every
forced transcript yields an ideal path with at most d false proposals.
For every fixed false proposal the checker error is at most epsilon. Then

    P(any false acceptance) <= min(1, J*d*epsilon).       (1)

For each possible disclosure transcript, run the ideal policy with that
transcript supplied externally. This gives at most d seed-independent
false proposals. Before the first error the actual path belongs to one of
these paths, so union bound over at most J*d fixed bad-check events proves(1).
Some forced transcripts may be impossible; counting them is conservative.
This is a description-length union bound, not a new leakage principle.

For k private degree-D polynomial checks on a q-point grid, q>D,

    k >= ceil(log(J*d/delta)/log(q/D))                  (2)

is sufficient for error at most delta. A fixed padded b-bit disclosure has
J<=2^b. Variable-length messages, timing and message counts must be included
in J, not treated as free. An indefinitely long cost transcript generally
has no finite J, so a fixed k does not automatically support it.

## A concrete safe implementation contract

Evaluate declared pure circuits in a trusted checker, expose no private
inputs, intermediate values, addresses, logs or early-exit indices, and use
a public work tariff independent of the hidden points. Counting every gate
of a fixed straight-line circuit on every sample meets the abstract gate-
count contract. It does not prove actual constant-time machine execution.
Alternatively retire the private batch before disclosing its detailed cost.
Padding and hidden checking still consume real resources and must be charged.
In the one/two-operation example, padding to2 costs one extra operation on
half the uniformly distributed points: mean overhead is1/2, or one-third
of the original mean1.5. That is the explicit price of this tiny repair.

A model given arbitrary executable code access to its checking inputs can
leak them directly; the pure bounded evaluator is therefore substantive.
These limits narrow applicability but preserve a useful synthesis: paid
computation, confidence reuse and the observable-information contract must
be designed together. Ordinary constant-time/checker and adaptive-data-
analysis methods are the relevant strong comparisons.
