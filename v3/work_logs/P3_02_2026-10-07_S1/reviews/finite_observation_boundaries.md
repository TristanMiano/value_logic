# P3-02 hostile review: finite codes and realized observations

Contributor: **ChatGPT (GPT-6 Astra Pro)**, independent subagent review,
October 7, 2026 UTC. These are direct mathematical boundary checks for P3-02,
not a new learner, statistical-rate result, later-task execution or added
research-time credit. Only this review is added.

Context inspected: the current principal derivation's exact finite recovery,
score calibration, noisy-conditioning and native-interface sections;
`reviews/scoring_sources.md` §§2–7; `reviews/noise_conditioning_case.md`;
and the already reconstructed phase-two finite-code/query distinctions in
`v2/derivations/06_n01_decision_retention.md` D20–D21. The proofs below do
not require importing another statistical theorem.

## 1. An N-code summary has sharp worst-case radius 1/(2N)

Let the encoder be any deterministic function

```math
h:[0,1]\longrightarrow\{1,\ldots,N\},\qquad N\ge1,
```

and let the decoder return a real number `d_j` for code j. It sees only the
code and fixed shared metadata; any additional p-dependent information is
part of a different interface. The encoder need not be linear, continuous
or measurable. Put

```math
R(h,d)=\sup_{p\in[0,1]}|p-d_{h(p)}|.
```

Every p belongs to the closed interval
`[d_{h(p)}−R,d_{h(p)}+R]`. Hence the N decoder-centered intervals cover
`[0,1]`. Their union has length at most `2NR`, so

```math
R(h,d)\ge\frac1{2N}.
\tag{F1}
```

This finite interval-cover argument requires no regularity of the code
fibers. Infinite R makes the lower bound trivial.

The bound is attained. Partition `[0,1]` into N equal-width bins, assign
each interior boundary consistently to either neighboring bin, and decode
bin j to its midpoint `(2j−1)/(2N)`. Every error is at most `1/(2N)`;
the interval endpoints attain it. Thus (F1) is the exact unrestricted
deterministic N-code minimax radius for this interface.

With at most B fixed-length binary bits, `N≤2^B`, giving the lower bound
`2^(−B−1)`. This is not a claim that a particular floating-point format
achieves the equal-bin optimum. Exact recovery of the entire continuum
is impossible with a finite alphabet, because its decoder has only finitely
many possible outputs. The result closes the arbitrary-nonlinear-real-code
loophole only after a genuine finite code budget is stipulated.

### Action labels may be much cheaper, with a computational condition

If the requested service is a fixed binary decision such as whether
`p≤1/2`, one bit can retain its answer exactly. A finite action menu can
similarly retain a chosen label using at most the menu's label count.
This does not reconstruct p and does not preserve answers after arbitrary
threshold, payoff or action-family changes.

The encoding claim assumes that the encoder can actually compute the desired
label from its permitted information. It does not grant free access to the
latent law, an exact expected loss or a computationally unavailable comparison.
Equal-width quantization likewise assumes an encoder capable of comparing
its available exact quantity with those bin boundaries. A finite realized
sample is a different access model and need not support that encoder.

## 2. Finite Bernoulli transcripts do not identify p by zero-error support

Let `X₁,…,X_n` be iid Bernoulli(p) with a fixed finite n and `0<p<1`.
For a particular binary transcript x containing k ones,

```math
\Pr_p(X=x)=p^k(1-p)^{n-k}>0
\quad\text{for every }p\in(0,1).
\tag{F2}
```

Therefore the set of interior p values compatible with x in the strict
**positive-likelihood, zero-error** sense remains all of `(0,1)`.
No deterministic decoder of that transcript can return the exact p for
every admissible parameter and possible observation. More strongly, the
supremum absolute error over that compatibility set is at least `1/2`
for every transcript; the constant output `1/2` attains this strict
worst-case radius. A deterministic confidence set with coverage one for
every interior p could not exclude any interior p on any transcript,
because that transcript has positive probability under the excluded p.

If endpoints p=0 or p=1 are admitted, a mixed transcript excludes both;
all-zero or all-one transcripts exclude the opposite endpoint. None of
these finite transcripts removes the whole open interval of possible laws.

### This does not say that the sample is uninformative

The likelihoods differ. For example, after n ones the likelihood ratio of
`p=3/4` to `p=1/4` is exactly `3^n`. The observation can strongly favor
one parameter while retaining nonzero likelihood under the other.
Confidence procedures with a nonzero failure allowance, likelihood-based
inference, posterior updating and asymptotic consistency concern different
guarantees. No new construction or rate for those procedures is asserted here.

Also avoid calling the Bernoulli model “statistically unidentifiable.”
The map from p to the **distribution of the transcript** is injective for
`n≥1`: its first-coordinate event probability is p. Knowing that distribution
and observing one draw from it are different information inputs. Equation
(F2) concerns the latter and its strict support-based guarantee.

For a nonconstant optimal-action label, the same issue can block exact
zero-error action recovery from a finite sample. If `p=1/4` and `p=3/4`
require different unique actions, every transcript remains possible under
both. Merely having enough bits to store the eventual label does not make
that label inferable from the transcript. A task with one common optimal
action across all compatible laws is a different, easy positive case.

The iid Bernoulli assumption is explicit. This argument does not model
logical uncertainty about one fixed mathematical sentence, or choose the
later project's observation/update procedure.

## 3. An exact affine recoding transports the entire observation contract

Let exact values be `y=Lp`, observed values `z=Lp+e`, with known error set
E. For known invertible T and known offset b, transport

```math
z'=Tz+b,\qquad y'=TLp+b,\qquad E'=TE.
```

Then, for every observation,

```math
\begin{aligned}
\{p:z'-TLp-b\in E'\}
&=\{p:T(z-Lp)\in TE\}\\
&=\{p:z-Lp\in E\}.
\end{aligned}
\tag{F3}
```

On normalized laws the transformed payoff matrix may equivalently be written
`L'=TL+b1ᵀ`. The offset is added to both the exact means and the observed
record; the error transforms by T alone. The same feasible laws, target
information and target-error radii survive when the target and its metric
are held fixed.

Transporting the full joint error set is the exact general recoding contract.
Replacing it by another set needs a separate equivalence or containment
argument. Special restricted sources can make some changes irrelevant to a
particular service, but that is not supplied by invertibility alone. A change
of coordinates may assist a numerical algorithm without improving the
information contained in the original noisy record.

### Preconditioning the P3-02 matrix moves the small denominator

For the current conditioning example, take `δ>0` and

```math
L_\delta=\begin{bmatrix}0&1&1\\0&1&1+\delta\end{bmatrix},
\qquad
T_\delta=\begin{bmatrix}1&0\\-1/\delta&1/\delta\end{bmatrix}.
```

The transformed exact rows are indeed simple:

```math
T_\delta L_\delta p=(p_2+p_3,p_3).
```

But with original box errors `|e₁|,|e₂|≤ε`, the transformed error is

```math
e'_1=e_1,\qquad e'_2=(e_2-e_1)/\delta,
```

and its **exact** set is the parallelogram

```math
E'=\{e':|e'_1|\le\epsilon,
             \ |e'_1+\delta e'_2|\le\epsilon\}.
\tag{F4}
```

In particular `|e'₂|≤2ε/δ`, with a correlation to `e'₁`. The `1/δ`
sensitivity was moved into the observation uncertainty; it was not removed.
Using the complete set (F4) gives exactly the original fibers and the same
sharp radius already derived in `noise_conditioning_case.md`.

### Resetting the transformed error budget can exclude the true law

Choose `δ=1/10`, `ε=1/100`, and law `p=(1/2,1/4,1/4)`. Its exact record
is `(1/2,21/40)`. Admissible original errors `(1/100,−1/100)` produce

```math
z=(51/100,103/200),\qquad
T_\delta z=(51/100,1/20).
```

The transformed p₃ error is `1/20−1/4=−1/5=−2ε/δ`. Assigning the old
`±1/100` budget to this apparently well-conditioned coordinate would exclude
the actual law. Its error satisfies (F4) exactly.

### Even the correct marginal error bounds can lose joint information

For `δ=2`, `ε=2/5`, and original observation `z=(4/5,7/5)`, write
`u=p₂+p₃` and `r=p₃`. The exact source has `0≤r≤u≤1` and
`u+2r≤9/5`, so `r≤3/5`. This is sharp: the laws
`(0,1,0)` and `(2/5,0,3/5)` are feasible and attain `r=0` and `r=3/5`.

The transformed observation is `(4/5,3/10)`. Replacing (F4) by its marginal
rectangle `|e'₁|≤2/5, |e'₂|≤2/5` admits the extra law
`(3/10,0,7/10)`, yielding the larger upper value `r=7/10`. Its transformed
error is `(1/10,−2/5)`, within those marginal bounds, but
`e'₁+2e'₂=−7/10` violates (F4). Thus carrying the amplified width while
discarding its joint constraint can still weaken the recovery service.

## 4. A sample-score decoder returns sample frequencies under its actual inputs

Fix reports/probes `q₁,…,q_m` and their known finite loss matrix
`L_{ji}=ℓ(q_j,i)`. For one realized outcome Y, scoring **all probes on that
same outcome** gives the column vector

```math
s(Y)=L e_Y.
```

If the known-loss decoder identifies every normalized law from its expected
loss vector, it necessarily maps this particular input to `e_Y`. That is
the point mass for the realized outcome, not the agent's earlier belief or
the population law that generated Y.

For one common batch `Y₁,…,Y_M`, the empirical average for each fixed probe
satisfies the deterministic identity

```math
\bar s_j=\frac1M\sum_{t=1}^M\ell(q_j,Y_t),\qquad
\bar s=L\widehat p,\qquad
\widehat p_i=\frac{\#\{t:Y_t=i\}}{M}.
\tag{F5}
```

An exact inverse therefore returns the **empirical law** `p̂`. No iid
assumption is needed for identity (F5); connecting that empirical law to a
population law with a useful statistical guarantee is a separate task.
The same conclusion holds for the current score calibration construction
when the shared affine score units are fixed over the common batch:
the input is `b1+sL p̂`, so the calibrated output is still p̂.

If the common stake varies between trials, averages can instead encode a
stake-weighted empirical law. With positive stakes `s_t` shared across probes
on trial t, its weights are proportional to `Σ_{t:Y_t=i}s_t`. Calling that
the unweighted empirical law would require an additional assumption.

### Separate probe batches need not form any exact expected-score vector

For binary Brier losses `ℓ(q,i)=||q−e_i||²`, pure reports `q=e₁,e₂` have
expected losses `(2p₂,2p₁)`, whose sum is always two. If the first probe is
scored on outcome 1 and the second on a different trial's outcome 2, their
realized score vector is `(0,0)`. Each observation is legitimate, but no
normalized law has that exact expected-score vector. One cannot run an
expectation inverse and grant its output population meaning. Separate-batch
estimation needs its actual sampling/error relation, or a common coherent
source with justified uncertainty.

Likewise, a learned vector of scores need not equal either `Lp` or `L p̂`.
It needs the declared estimation/adequacy contract. Knowledge of the entire
distribution of realized scores is yet another input: it can recover a law
when the outcome-to-score map is injective, even if one scalar expected score
would not have sufficient rank. These statements concern distinct information
objects, not competing definitions of the same value.

## 5. Integration judgment

The four proposed boundaries survive direct reconstruction. The finite-code
bound quantifies what exact-real rank calculations do not address; the finite
transcript argument separates strict zero-error compatibility from useful
statistical evidence; correct preconditioning preserves the noise geometry;
and sample-score inversion recovers the law actually represented by that
sample vector. All are ordinary mathematical consequences under their stated
interfaces. They provide no claim of a new learner, new statistical rate,
P3-03/06/07 result or automatic contribution support.
