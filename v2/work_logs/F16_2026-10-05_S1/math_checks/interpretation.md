# F16-MATH-01 — exact verification interpretation

**Signed: ChatGPT (GPT-6 Astra Pro). October 5, 2026 UTC.**
This is a bounded mathematical verification of the F16 correction and optional
decoder theorem. It is not F15 evaluation data, ND01 diagnostic data, a new
neural recurrence, or a statistical test of generalization.

## Outcome and reproducible command

The one declared execution completed on attempt 1 with exit 0, empty stderr,
and **1,439 passing records** in four specified families. No retry or expansion
was used. The design was saved before execution; its hash, the executed source
hash and the saved-certificate input hash are in `attempt1/manifest.json`.
The exact executed source is preserved as `attempt1/source.py`.

From the repository root, the executed command was:

```bash
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1 python v2/work_logs/F16_2026-10-05_S1/math_checks/check_math.py > v2/work_logs/F16_2026-10-05_S1/math_checks/attempt1_stdout.txt 2> v2/work_logs/F16_2026-10-05_S1/math_checks/attempt1_stderr.txt
```

The script refuses to overwrite `attempt1`. Reproduction should use an isolated
export with the saved output directory absent; no new F15 directory, stage,
seed or model is involved. Its only numerical operations use exact standard
library fractions. The recorded environment is CPython 3.12.14, NumPy 2.3.5
installed, Linux x86_64 and the prescribed single-thread variables.

## What was checked

| Family | Records | Interpretation |
|---|---:|---|
| Exact k=3 old-summary fibers | 656 | Every eight-part probability composition with denominators 1, 2 or 3, at four declared positive penalties. Full world-mass constraints, proper midpoints, old means, direct stopped-cost semantics and the canonical common-radius decoder were checked. |
| Previously saved candidate certificates | 735 | An independent reader reconstructed the two-support extrema and checked each saved candidate, normalization, mean, moment values and radius. This validates saved finite evidence; it does not count it as a second independent experiment. |
| Global formula | 45 | For k=2,...,10 and five fixed penalties, independent three-level diameter enumeration agreed with singleton dominance, the scalar formula and the discrete maximizing-index rule. |
| Exact boundary witnesses | 3 | The k=3 terminal midpoint differs, the k=4 coordinate-midpoint law remains invalid, and the k=4 canonical common-radius law is valid. |

The k=3 family made 23,616 direct edited-order checks: three edited indices,
two signs and six permutations per record. Each direct cost was obtained by
stopping at the first success on each world, rather than importing the frozen
moment-cost implementation. Repeated laws across denominators were specified
in advance and remain counted as records, not independent populations.

The coverage is deliberately small and exactly described:

| Fiber dimension | Exchangeable input | Nonexchangeable input |
|---|---:|---:|
| 0 | 24 | 588 |
| 2 | 20 | 24 |

Thus 44 fibers have positive planar area, including 24 with nonexchangeable
offsets; 612 are point fibers. These numbers are not a representative sampling
claim. For an unrestricted exact k=3 old-summary fiber, the canonical residual
description explains the absence of one-dimensional examples: zero residual
mass or an endpoint residual mean gives a point, while positive residual mass
and an interior mean give a two-dimensional simplex section. The general
planar lemma also handles degenerate segments when additional convex
constraints are considered, but no such extra constraint was added here.

The source code enumerates all rational vertices of the two-dimensional
world-mass inequalities. Checking affine objectives at those vertices gives
their extrema for that particular fixture. The compatible-law and midpoint
checks therefore concern whole fixture fibers, not only the originally chosen
law. This is still finite evidence across fibers; the proof supplies the
universal quantifier.

## Meaning of the new result

In k=3, the separate planar proof shows that all proper moment midpoints are
jointly feasible. For the general equal-price family, the new proof instead
uses the average of a singleton-minimizing endpoint law and a
singleton-maximizing adjacent-level law. It need only attain the **common
maximum error tolerance**. It need not place every narrower coordinate at
its own midpoint.

The old k=4 example makes this distinction exact. Its individual-midpoint
inversion still assigns -3/496 to a specified world. The new compatible
candidate shifts the pair prediction by -1/1488 from that pair's midpoint
while retaining the same common radius 21/496. There is no contradiction or
reason to delete the old negative-mass witness.

Neither a compatible minimax law nor these checks identify the true unknown
population law. They also say nothing about whether an ordinarily trained
network uses a particular internal cost representation. F15's 0/5 complete
neural endpoint and all retention counts remain unchanged.

## Resources and limitations

Recorded process wall time: **2.082920667 seconds**; user CPU **2.068908**;
system CPU **0.011490**; Linux peak RSS **19,116 KiB**. These are one-process
resource observations, not comparative benchmarks. The principal clock
excluded the initial blocked wait; the remainder overlapped active principal
derivation and was not added a second time as research effort.

All 1,439 records are durably saved. Their SHA256 is
`5d17dc5957ab2ab5eacba4cb1d1d0bca98294ceb2159b6184cc6c096d197dc70`.
The saved 735-record input hash is
`50eea75059d727e85edda2a8178f7730f1aa903e24283dafed1d3ffdfa981902`.
The generated manifest and summary contain further environment and resource
fields. The checks establish neither worldwide priority, numerical conditioning
at floating precision, empirical calibration nor a speed advantage over
ordinary exact optimization.
