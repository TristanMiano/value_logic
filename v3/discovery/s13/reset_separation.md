# Costly resets separate parity acquisition from complete reconstruction

Codex (GPT-6), DEVELOPMENT, October20,2026. Combines the inherited ordinary
cost-alphabet entropy bound in s12/invoice_entropy.md with invoice_rate.md.
It is a task distinction inside the stipulated channel, not a new coding law.

Each nonempty episode has at most H public invoice values and costs at least
f+1. Full reconstruction of n fair independent bits therefore requires
expected fee at least n*(f+1)/log2(H). This follows from the stronger inherited
bound n/a, where sum_(k=1..H) 2^(-a*(k+f))=1. Stop decisions and episode counts
are functions of the public transcript, not additional free outputs.

In contrast, the parity construction with r=H-2,d=1 has leading rate
(f+H-1/2)/(H-1). For H>=4, H-1>log2(H). The full-vector lower bound exceeds
this parity upper rate whenever

```math
f>\frac{(H-1/2)\log_2H-(H-1)}{H-1-\log_2H}.
```

For H4 it suffices that f>4. At f5, parity costs at most(17/6)*n+O(1),
whereas complete reconstruction costs at least3n. Hence the two objectives
have provably different leading fees in this regime, assuming the proposed
parity result. The stronger alphabet-root lower bound can separate them sooner.

The parity prelude is useful because it retains an aggregate while discarding
individual bits. That is compatible with the program's decision-relative goal;
it does not show superiority over ordinary function computation at the same
interface. No matching positive-reset full-vector rate has been proved here.
An encoder that already knows a message can select arbitrary timing codewords;
our private program must first purchase the bits that determine its invoice.
This extra realizability restriction prevents importing a timing-channel
capacity as an attainable acquisition rate.
