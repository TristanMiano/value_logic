# Exact Bernoulli mixture intervals at sparse count epochs

**DEVELOPMENT — Codex (GPT-6), October 14, 2026 UTC.**
Prospective repair of the conservative continuum learner. Statistical
mixture confidence sequences are established methods; this derivation makes
the exact arithmetic and outward rounding explicit for the receipt service.

For n compulsory-pair samples with s repeats, the likelihood at p is
L_n(p)=p^s(1-p)^(n-s). A uniform mixture over p in [0,1] has likelihood
M_n=1/((n+1) choose(n,s)). For any fixed true p in (0,1), M_n/L_n(p)
is a nonnegative unit-mean likelihood-ratio martingale. At p=0 or 1 the
corresponding process is a nonnegative supermartingale on possible data.
Ville's inequality therefore gives simultaneous coverage for

```math
C_n=\{p\in[0,1]:20(n+1){n\choose s}p^s(1-p)^{n-s}\ge1\}
```

at level at least 19/20. Intersecting successive C_n retains that same
common-event guarantee. A fixed p's likelihood is unimodal, with its maximum
at s/n, so C_n is one closed interval containing the empirical fraction.

Use a fixed dyadic grid D=4096. At grid point k/D, membership reduces to the
integer comparison

```math
20(n+1){n\choose s}k^s(D-k)^{n-s}\ge D^n.
```

Binary search on each side of s/n finds grid brackets. Round the lower
endpoint down and the upper endpoint up. If no grid point on one side of
the mode is accepted, the neighboring mode grid cell remains a safe outer
bracket. Treat 0^0 as one in the likelihood formula. At n=0 return [0,1].
The result is an outer interval for C_n; no floating-point logarithms or
approximate root solver are trusted for coverage. Integer powers and their
operand lengths belong in the statistical invoice.

First compare the returned intervals with direct rational membership across
n=0..64 and all s, and compute exact finite-horizon first-rejection
probabilities for several true p values. The latter are sanity checks of
the common-event argument, not a replacement for it. Then change only the
confidence routine in the continuum service, preserving its old sources,
1,024 rows, seeds, epsilon, bins, policies, original outputs and declarations.
Run only the learner and identical ordinary mirror as an exposed-row
ablation. Setup and all failed prefixes remain charged or explicitly unknown.
