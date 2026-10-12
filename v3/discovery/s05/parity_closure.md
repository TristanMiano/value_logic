# Executable parity-error closure

Contributor: **ChatGPT (GPT-6 Astra Pro)**. October 12, 2026 UTC.
DEVELOPMENT. This is a new component of the open discovery portfolio.

## Constructive result and its use

The [derivation](calibration_branches.md) establishes an exact information
boundary. Given only simultaneous upper bounds `u_ab` on disagreement of
common vertex error bits, the largest possible error of an even parity target
`T` is `min(1, minimum u-weighted T-join)`. It follows by packing odd cuts and
the established T-join dominant description, not by assuming independence.
The [primary-source notes](sources.md) distinguish the imported graph theorem
from this application to calibrated errors.

On a physical tree with only edge marginals, the old sum-of-errors bound is
already sharp for each target. A better guarantee requires additional
information: useful block errors, direct target audits, or justified source
structure. This gives a concrete reason to investigate how evidence is bought.

The new [implementation](parity_closure.py) returns a checkable set of pair
receipts, its boundary and total error weight. It uses all-pairs shortest
paths plus subset matching for a small target boundary. The implementation
cost is exponential in boundary size; no large-boundary scaling claim is made.
General minimum T-joins admit the conventional matching approach. Acquiring
the error bounds and evaluating their consequences are separately billed.

## Small constructive probe

Run from the repository root:

```bash
python v3/discovery/s05/parity_probe.py
```

The [recorded result](parity_results.json) binds both source files, seed,
environment, inputs, returned joins and finite-world extremizers. On 176 small
cases with 2–7 vertices, the graph closure and direct optimization over all
rooted bit assignments agree to maximum absolute difference
`1.1102230246251565e-16`; the reported inequality residual is zero. This is a
development check of the implementation and examples, not a new proof or an
economic experiment. The direct finite-world LP has exponential size.

The cancellation example improves a population error bound from 0.8 to zero
by adding two block-error observations. Those observations are assumptions in
that illustration. The same note shows why auditing the single fixed target
can cost less than buying reusable blocks. The `K_(2,3)` example separately
shows individual sharp bounds summing to 2.8 while the maximum jointly
attainable sum is 2.4. Individual sharpness does not establish exact value
planning for several targets at once.

## Paid-source connection

For true vertex signs `X_v`, a product of edge parities over a forest equals
the product of signs at its odd-degree boundary. Internal signs cancel.
Thus a block can often be measured by purchasing its endpoint truths, while
reusing any already checked receipts. An unknown anchor must still be bought;
the CNF adapter does not provide a free root truth.

[The real CNF adapter](cnf_receipts.py) makes this interface concrete. Its
receipt includes a checked answer and, when available, a SAT witness or a
transported UNSAT justification. Such payloads can lower later work even when
their vertex cancels from the algebraic target. Consequently the acquisition
price is a function of the current receipt state and purchase order. The
error-weighted calibration graph is not a graph of fixed evaluation prices.

Retain the [adaptive calibration options](adaptive_calibration.md), direct
paired-policy auditing and source-specific proof acquisition as alternatives.
No deployment policy has been promoted; P3-POS01 remains outstanding.
