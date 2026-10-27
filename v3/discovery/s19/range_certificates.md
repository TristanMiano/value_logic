# Rational certificates for a complete attainable range

Codex (GPT-6), October 26, 2026. DEVELOPMENT. This is a proposed checked
implementation boundary for anchor_ranges.md, using standard LP duality.
The complete-range algorithm is the candidate; rational dual certificates
are established machinery and do not independently support a novelty claim.

For each generator and receipt subset, the checker itself constructs the
local inequalities A*x <= b from the original source and receipt records.
The proposer must supply exactly one entry for every one of the n*2^k
slices. Omitting an inconvenient slice could create a false gap and must be
rejected. The original problem digest is supplied independently of the
certificate; a self-reported digest alone cannot authenticate the premises.

Write the target as c*x+d. A bounded entry contains points x_minus,x_plus,
values ell,u and nonnegative dual vectors lambda_minus,lambda_plus. Check

    A*x_minus <= b; A*x_plus <= b;
    c*x_minus+d = ell; c*x_plus+d = u;
    A^T*lambda_plus = c; b^T*lambda_plus+d = u;
    A^T*lambda_minus = -c; -b^T*lambda_minus+d = ell.

These identities prove both extrema directly: for every feasible x,
-c*x <= b^T*lambda_minus and c*x <= b^T*lambda_plus. The supplied primal
points establish attainability. No trust in a numerical solver status or
its floating-point tolerance is required.

An infeasible entry supplies lambda>=0 with A^T*lambda=0 and b^T*lambda<0.
If a feasible x existed, multiplying its inequalities would give
0<=b^T*lambda<0, a contradiction. This also has a direct exact check. A
missing or invalid certificate leaves the range unverified; it cannot be
relabelled as an empty slice. Inconsistent global observations produce an
explicit empty-source status, not an action warrant over an empty domain.

After checking every slice, recompute the prefix/suffix bottlenecks and
anchored intervals. Compare the complete normalized interval list with the
proposed output. This catches both invented values and deleted components.
For a proposed attained value, source reconstruction and direct checking
against the original inequalities are an additional concrete witness path.

The proof checker uses rational arithmetic. Its bill depends on certificate
length and integer bit lengths as well as the combinatorial DP; it is not
constant overhead. It assumes the input polytopes, affine response semantics,
versions and observation bounds have the intended external interpretation.
Checking linear algebra cannot establish those empirical premises or prove
the correctness of the Python runtime/hardware. The current host's retry
allowance does not excuse deterministic certificate failures.

A bounded development producer can use exact two-dimensional geometry and
enumerated supports to supply primal and dual certificates. The checker
need not share that geometry implementation and can accept arbitrary finite
dimension when the supplied certificates meet the displayed identities.
A general scalable certificate producer is a separate integration duty.

## Executed development bundle

[Plan](range_cert_plan.json), [producer](range_cert_probe.py),
[verifier](range_cert_verify.py), [bundles](range_cert_bundles.json),
[result](range_cert_result.json). Producer hash
24505901277ea4d4e57016fa5fdabbd1ee773d69dd709c995d38cce92987480c; verifier hash
5ea2d439760170d1c60be0233a6394e5a181fbfcb2ea1e0738ee85751039136a.
Bundle hash11094afed00f3620ad1f03e20a84d3b720988589ee4a52431498a78e270a0f32.

PASS:44 bundles,854 bounded slices,336 infeasible slices and21,785 dense dual
entries. Five inputs have inconsistent sources. All273 deliberately altered
certificates were rejected:44 missing slices,44 invented ranges,44 changed
problems,40 wrong endpoints,40 negative multipliers,40 wrong primal points,
19 false empty-slice certificates and2 deleted range components. Two explicit
three-dimensional boxes exercise the verifier beyond the polygon producer.

This reuses the first40 exposed polygon inputs, plus two known gap cases and
the explicit boxes; it is development, not fresh independent confirmation.
The bundle occupies874,838 bytes. Measured production997,649,100ns and valid
verification191,130,300ns are separate parts of a1,489,820,600ns total probe;
the remainder includes mutation checks and I/O. None is an extra research-
clock credit or a comparative solver performance claim.
