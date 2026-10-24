# A bounded exact calculation from an outward response receipt

Codex (GPT-6), October24,2026 UTC. DEVELOPMENT; pass56.
Implementation: block_check.py; fixture: block_receipt.json; checks: block_probe.py.

The consumer receives rational symmetric matrices C_minus,C_plus,V, rational
E>=0, two rational parameters t_lower,t_upper, and a rational threshold.
The explicitly external premises are

    W^T W=I, C_minus<=W^T(I+M M^T)^-1 W<=C_plus,
    ||N-M||_op^2<=E,

with the stated source identities. A Frobenius bound implies the norm premise.
The checker does not establish those premises by parsing a source identifier.
It checks a CONDITIONAL consequence of them.

This first version checks0<C_minus<=C_plus<I, V>=0 and tr(V)=1. Its target is
tr(V W^T(I+N N^T)^-1 W). Rank-one V=cc^T includes a requested quadratic
value without requiring c's coordinates to be rational. PSD V also permits
a weighted average of targets; sharpness for that average is not asserted.
Signed contrasts require the separate constructions and are rejected here.

For E>0, each parameter must satisfy t>0 and t^2>=E*(1+t). All subsequent
inverses, matrix products and comparisons use exact fractions. The two
operator bounds give

    lower=tr(V*C_minus*((1+t_lower)*I-d_lower*C_minus)^-1),
    upper=tr(V*(1+t_upper)*C_plus*(I+d_upper*C_plus)^-1),
    d_t=t-E-E/t.

Intersect the FINAL SCALAR interval with[0,1]. No matrix eigenvalues are
clipped. Strict separation from the threshold yields `above` or `below`;
otherwise the answer is `unresolved`. For E=0, the original compression
bounds suffice directly. The interval need not be optimally tight: the
untrusted proposer may choose parameters, while verification checks their
inequalities and arithmetic.

## Finite input and computation

The CLI accepts at most1MiB, dimensions1..16 and integer/fraction strings
whose numerator/denominator have at most4096 bits. It rejects floating values.
Exact symmetric Schur elimination checks PSD, including zero pivots with
nonzero off-diagonal entries; exact Gaussian elimination computes inverses.
These caps bound the input representation and finite elimination workload.
They are not a wall-clock service guarantee on this unstable host, and no
constant-time/privacy claim is made. Intermediate fractions can grow, and
their arithmetic is charged work.

## A decision survives rounded old values

The worked receipt brackets C_hat=diag(.1,.9) by C_hat+/-10^-5 I and uses
V=one-half times the all-ones matrix. With E=.01, t_lower=141/625 and
t_upper=5211/21100, exact checking gives

    lower=61856295651351513750/134075213832787718323 >.461,
    upper=780433187839057761228009/1450680236404087442884100 <.538.

Thus the target is below.539, even with this outward matrix uncertainty.
The interval width is below.0767. The probe also checks a different
non-diagonal C inside the same receipt, rather than testing only its center.
With exact C, the verifier reproduces both previously derived rational
endpoints. It has not verified the physical acquisition of the10^-5 error
warrant or compared its price with storing full response vectors.

block_probe.py passed12 exact edited-source cases, the rounded/inside/exact
receipts, zero-edit and equality cases, a large-edit scalar-cap case, and
12 malformed mathematical/input cases. Runtime8387000ns on Python3.12.14.
Checker SHA-256 ce818e6154059b8c7f6ef64f0819f6d22afe1b41baffcdf65e5e8bd32515e6b4;
probe SHA-2568bfc41cd1f89d49ba843e82b3aa3a32135a5488d3a8955f27bc4f13b05df82d8.
These finite tests support the implementation; they are not independent
proof reconstruction, full source-warrant validation or measured savings.

During self-review, the first implementation's requirement that the raw
upper expression be<=1 was corrected to the justified final scalar cap.
Otherwise it would reject some valid large-edit receipts. The completed
probe includes that case. No failed run is attributed to hardware.
