# P3-02 targeted reconstruction: native probability-information interface

Contributor: **ChatGPT (GPT-6 Astra Pro)**, independent subagent review,
October 7, 2026 UTC. This is a mathematical reconstruction using the existing
rules, not an executed new certificate producer or checker test. No overlapping
time is credited; no phase-two file or gate is changed.

## 1. Contract and exact records

The partial `v3/derivations/02_probability_information.md` proves mathematical
recovery from known finite losses. This note checks exactly when that recovery
has a native certificate. The distinction is between an external decoder, a
native proof in the loss unit, and a native proof whose root is actually in
the probability unit.

Load-bearing definitions are:

* `v2/foundations/03_provisional_core.md` §§2–4: source identity, rational
  positive named conversions, valuation bridges, rational CPWA terms and
  nonempty closed rational polyhedral cases.
* `v2/derivations/02_inference_rules.md` §2: R0 constant difference, R1 source
  row, R2 exact difference rewrite, R4 addition, and R5 nonnegative scaling,
  polarity reversal and declared conversion. A source equality requires both
  inequality orientations.
* `paper_v2.md` §§5.1–5.2: current-request soundness and target-unit-reduct
  completeness. A reverse conversion is not invented by proof search.
* `v2/derivations/04_characterization.md` §§9–12 and
  `04g_characterization_acceptance.md` §3: actual unit transport followed by
  rational nonnegative row multipliers yields a native affine certificate.
* `v3/foundations/01_representation_boundaries.md` §1: jointly varying
  coefficient/probability products are not generally in the exact grammar.

Below, `t <=[b] s : U` means that the native root bounds `t−s` by rational
budget `b` in unit `U`. The units denote copies of the real line; a probability
unit label alone does not impose nonnegativity or normalization. Those are
explicit source constraints.

## 2. Concrete loss inversion without an illicit reverse arrow

Let `p:P` be an event probability coordinate and `y:U` its expected-loss
coordinate. On the event the known loss is `5_U`, off it `1_U`. Declare only
the forward valuation bridge

```math
w:P\longrightarrow U,\qquad w(x)=4x.
```

The expected loss is `y=1_U+w(p)`. The numerical expectation observation is
`2_U≤y≤3_U`. Use one source case with these explicit affine rows:

| Row | Unit | Inequality |
|---|---|---|
| P0 | P | `−p≤0` |
| P1 | P | `p≤1` |
| U0 | U | `y−w(p)≤1` |
| U1 | U | `w(p)−y≤−1` |
| U2 | U | `y≤3` |
| U3 | U | `−y≤−2` |

The rational witness `p=3/8, y=5/2` makes the case nonempty. The observation
and the expectation identity are source assumptions with the declared common
population/payoff meaning. A learned estimate does not supply these rows as
exact population equalities without an additional justification.

### A valid native loss-unit proof

R1 introduces U1 and U2. R4 adds them, and R2 cancels the common `y`, giving

```math
w(p)\le[2]0_U.
\tag{N1}
```

Similarly U0+U3 gives

```math
-w(p)\le[-1]0_U.
\tag{N2}
```

The arithmetic budgets are `−1+3=2` and `1−2=−1`. Negative budgets are
retained exactly. Numerically these establish `1≤4p≤2` throughout the
full source, hence externally `1/4≤p≤1/2`.

### What is not a native probability-unit proof

With only `P→U`, the `P`-reduct removes every U row. It retains P0 and P1.
The assignment `p=3/4, y=5/2` satisfies that reduct and refutes `p≤1/2`.
Therefore, by the inherited exact characterization, the current native
calculus cannot produce that probability-unit root from this signature.
This is not a proof-search timeout; it is a reduct countermodel.

The external arithmetic division by four is correct. Calling it an existing
native `U→P` proof instruction would be incorrect. The forward bridge is a
valuation choice, not an automatic assertion that every loss quantity is a
probability in another unit.

### Two allowed completion routes

**Explicit reciprocal calibration.** If the context really declares and
justifies a reverse numerical calibration `r:U→P` with factor `1/4`, R5
converts (N1), including its budget, to

```math
r(w(p))\le[1/2]0_P.
```

R2 uses the actual product of declared factors, `(1/4)·4=1`, to rewrite the
root as `p <=[1/2] 0_P`. Converting (N2) gives
`−p <=[−1/4] 0_P`. Both are now native probability-unit bounds. The scope
must record this numerical calibration; it need not pretend that a monetary
cost is universally interchangeable with a probability.

**External calibrated adapter.** Keep (N1) and (N2) as loss-unit roots, and
have an explicitly specified external semantic adapter check their fixed
payoff meaning and infer the probability interval. This delivers a valid
conditional probability result but the native roots remain in U. If the
adapter creates a new probability-source row, that row is a newly justified
premise in a new context; it was not derived by an undeclared native inverse.

These routes have different proof and interface claims even though they
return the same numerical interval.

## 3. Finite-law constraints and a full row-span certificate

For world probabilities `p_i:P`, declare `−p_i≤0` and both orientations of
`Σ_i p_i=1`. A known loss row in unit U can be written as
`Σ_i L_i ι(p_i)` using a declared factor-one bridge `ι:P→U`, with each `L_i`
a fixed rational number in the chosen payoff table. More generally, for a
declared factor `κ>0`, use coefficients `L_i/κ` on the converted coordinates.
This is finite affine syntax, including when a payoff coefficient is negative.

An exact observed expectation `y_j` is two source rows; a justified interval
is two possibly nonmatching endpoint rows. Measurement coordinates, payoff
rows and event coordinates keep their source identities and evidence revision.
Rows in different loss units can participate in one native conclusion only
through actual directed paths to its target unit.

For clarity, suppose the following numerical rows have legitimately been
transported into P using declared calibrations, or supplied in P by an
explicitly justified external observation adapter. Define

```math
s=p_1+p_2+p_3,\qquad
\ell_1=p_1+2p_2,\qquad
\ell_2=p_2+3p_3.
```

Retain the two orientations of `s=1`, `ℓ₁=5/4`, `ℓ₂=5/4`, plus
nonnegativity. The feasible rational witness is
`p=(1/4,1/2,1/4)`. Its normalization-augmented matrix is

```math
\begin{bmatrix}1&1&1\\1&2&0\\0&1&3\end{bmatrix},
```

with determinant four. The row-span reconstruction is

```math
p_1=\tfrac32s-\tfrac12\ell_1-\tfrac12\ell_2,
\quad
p_2=-\tfrac34s+\tfrac34\ell_1+\tfrac14\ell_2,
\quad
p_3=\tfrac14s-\tfrac14\ell_1+\tfrac14\ell_2.
\tag{N3}
```

For an explicit native certificate of `p₁≤1/4`, introduce these source rows
and multiply them by nonnegative rational weights:

```math
\tfrac32(s\le1),\qquad
\tfrac12(-\ell_1\le-5/4),\qquad
\tfrac12(-\ell_2\le-5/4).
```

R4 adds them and R2 uses (N3); the resulting budget is
`3/2−5/8−5/8=1/4`. Using the opposite source orientations gives
`−p₁≤−1/4`. Apply the same construction to the other identities to obtain
`p₂=1/2` and `p₃=1/4` as pairs of native inequalities. Negative coefficients
in (N3) select the other equality orientation; they do not authorize the
unsound rule of multiplying an inequality and its budget by a negative
number while preserving its direction.

Generally, a supplied rational row-span witness
`q=α1ᵀ+Σ_j β_j L_j` yields the exact target value
`α+Σ_j β_j y_j` by this same construction. Constants use R0 if the chosen
query presentation includes an explicit offset. The proof checks the
coefficient identity and recomputes the budget from the actual source rows;
it does not trust a decoder's final answer alone.

All these conclusions are conditional on accessible, correctly interpreted
source rows. Simply writing the numerical matrix in P cannot itself justify
transporting an inaccessible U observation into P.

## 4. A sharp interval with explicit endpoint and multiplier witnesses

Full-law recovery is unnecessary for a native probability interval. On the
three-world simplex, suppose the accessible observation is

```math
p_2+2p_3=\tfrac12.
```

The source is nonempty, but does not determine `p₃`. For the upper bound,
add the source rows `p₂+2p₃≤1/2` and `−p₂≤0`, then scale by `1/2`. The
native root is `p₃ <=[1/4] 0_P`. The source row `−p₃≤0` supplies the lower
bound. Hence

```math
0\le p_3\le\tfrac14.
\tag{N4}
```

The rational endpoint witnesses `(1/2,1/2,0)` and `(3/4,0,1/4)` establish
that the interval is sharp. They provide separate evidence for sharpness;
the native upper-bound proof itself only establishes validity.

This is an ordinary polyhedral identification calculation with a concrete
native realization. For a general accessible rational source `Ax≤b`, an
affine upper bound is certified by rational multipliers `λ≥0` satisfying
the exact coefficient identity and the requested RHS inequality. R1, R5,
R4, R0 and R2 replay that witness. The constructive completeness theorem
ensures such a proof exists for a finite valid bound on the target reduct;
it neither supplies free optimization nor guarantees that a bounded producer
will find it. In several live source cases, each case needs a proof of the
same literal target, followed by the inherited all-cases rule.

## 5. Common unknown stakes: affine threshold proof, external calibration

Let `v_i:U` be expected losses for an exhaustive event partition. The
separately justified semantic contract says

```math
v_i=s p_i,\qquad p\in\Delta_n,\qquad s>0
```

with the **same** stake `s`, constant across worlds for this valuation.
Then `S=Σ_i v_i=s` and externally `p_i=v_i/S`. This semantic bridge is
not an admitted bilinear native source equation in varying `s,p_i`.

For a fixed rational threshold `t`, however,

```math
p_i\ge t\quad\Longleftrightarrow\quad tS-v_i\le0
\tag{N5}
```

under that calibration and positivity premise. The right side is a native
affine loss-unit query. It uses only addition and fixed rational scaling;
there is no division or reverse unit conversion in its proof.

For a concrete two-event source take
`2≤v₁≤3`, `1≤v₂≤2`, all in U. It admits witness `(v₁,v₂)=(2,1)`.
Adding upper `v₂≤2` and lower `−v₁≤−2` gives `v₂−v₁≤0`; scaling by
`1/2` proves `(1/2)S−v₁≤0`. Separately, `(1/4)(v₁≤3)` plus
`(3/4)(−v₂≤−1)` proves
`v₁−(3/4)S≤0`. The native sign certificates, interpreted through (N5),
give

```math
\tfrac12\le p_1\le\tfrac34.
```

The endpoints are attained by `(v₁,v₂)=(2,2)` and `(3,1)`, respectively.
The same native source proves `S≥3`, so the denominator has a strictly
positive rational lower bound. The returned probability interval still
depends on the common-stake semantic contract. Arbitrary nonnegative values
can always be normalized into some mathematical vector in a simplex; that
alone does not identify the original agent's probability law.

Closed rational source cases do not directly express the open assumption
`S>0`. When positivity is to be established natively, supply or derive
`S≥δ` for a known rational `δ>0`; otherwise retain `S>0` as an explicitly
external bridge assumption. A native proof of the sign query can still be
valid without positivity, but its ratio interpretation cannot include zero.
For known negative S the sign reverses. Unknown sign needs separate cases
or another source contract.

This establishes an executable **form** of threshold query without claiming
a new ratio term, new source rule, performed checker run, or a native P-unit
root. If exact concrete rational `v_i` are supplied, an external constructor
can compute their rational normalized outputs; its arithmetic and calibration
remain explicit parts of the interface.

## 6. Uncertain payoff coefficients versus known random statewise stakes

With independently varying stake `s` and probability `p`, the product
`sp` is not generally finite CPWA. Introducing a source `z` does not prove
the relation `z=sp`. Fixed rational stake cases are affine; finitely many
supplied stake cases can be separate declared contexts. A continuum of
stakes needs a valid enclosure, another representation or a proved extension.
Turning such uncertainty into a random variable is a modeling choice, not
an arithmetic fix that preserves every original interpretation.

In contrast, consider a known finite world table with event E and stakes
one or three:

| World | E? | Known stake | Event-contingent loss |
|---|---|---:|---:|
| 1 | yes | 1 | 1 |
| 2 | yes | 3 | 3 |
| 3 | no | 1 | 0 |
| 4 | no | 3 | 0 |

Under an unknown joint law p, the expected event loss is the affine row
`p₁+3p₂`; expected stake is `p₁+3p₂+p₃+3p₄`, and event probability is
`p₁+p₂`. Every coefficient is fixed and rational. These quantities fit the
native affine grammar after the appropriate declared valuation conversions,
without assuming independence between stake and event.

Two admissible joint laws illustrate the information boundary:

```math
p^A=(0,1/2,1/2,0),\qquad
p^B=(1/2,1/3,0,1/6).
```

Both have expected event loss `3/2` and expected stake `2`, but their event
probabilities are `1/2` and `5/6`. Dividing loss by mean stake produces `3/4`
for both and recovers neither original event probability. The common-scale
calibration in §5 does not apply to statewise varying correlated stakes.
The obstruction here is the omitted joint information, not nonexpressibility
of the known finite loss table.

## 7. Result and remaining interface obligations

The existing native calculus can check finite rational probability recovery
and intervals using ordinary source-row arithmetic whenever the needed rows
can reach the target unit. It can also certify certain normalized probability
thresholds directly as affine signs in the loss unit, with an explicit
external calibration theorem interpreting the result. Neither construction
requires a general native division operation.

Every actual receipt must still bind the checked root to the current source,
evidence revision, population/payoff scope, case coverage, literal expression
pair, unit and requested budget. This reconstruction supplies the mathematics
and explicit rule skeletons; it does not claim a new serialized producer,
empirical calibration guarantee or executable test result. The ingredients
are inherited rules plus an ordinary finite-expectation adaptation, not
independent support for P3-N01.

## 8. Executed development follow-up

After the mathematical reconstruction above, a narrow executable check was
added at `v3/checks/02_native_probability_check.py`. The inspected
`v2/verification/native.py` and `model.py` wrappers are specific to the old
quartic experiment, so their Evidence/Query schema was not reused. The new
fixtures instead use the unchanged underlying F06 checker, F07 receiving
check/reference interpreter, and F08 unit-reduct, affine-certificate and
converted-proof adapters. No phase-two source was modified.

Actual command, from the repository root:

```bash
python3 -B v3/checks/02_native_probability_check.py --output v3/work_logs/P3_02_2026-10-07_S1/development/native_probability_agent.json
```

The first run completed with exit code **0**, under **CPython 3.12.14**.
Its observed start was `2026-10-07T04:30:34.658122+00:00`. This is execution
provenance, not additional research-time credit. The report preserves the
command arguments, interpreter identity, direct tooling/source hashes, source
contexts, complete proof traces, root requests, actual rejection messages and
finite reference-audit counts.

| Development group | Actual result |
|---|---|
| One-way binary bridge | Two U-unit bounds accepted; the P-reduct countermodel is feasible only in the reduct; a bare U-to-P rewrite is rejected. |
| Declared reciprocal calibration | Two P-unit receipts establish `1/4≤p≤1/2`. |
| Full three-state reconstruction | Six P-unit receipts establish all three exact probabilities, using both equality orientations and nonnegative multipliers. Converted proofs are grafted back and bound to the original current context. |
| Unsound negative multipliers | Both the native negative-scale mutation and the affine emitter's negative weight are rejected. A feasible source point also refutes the mutation's purported conclusion. |
| Fixed common-scale thresholds | Three U-unit receipts establish `S≥3` and the two affine signs interpreting `1/2≤p₁≤3/4` under the external calibration premise. |

Totals: **five groups passed, thirteen accepted target receipts, three
expected rejections**, plus the explicit reduct countermodel. The stored
direct-tooling hashes were compared with the files after the run and all
matched. This is supplied-fixture development evidence; it is not a general
producer, broad regression-suite run, frozen challenge, source-calibration
experiment or new native division rule. The mathematical limits in §§1–7
remain unchanged.
