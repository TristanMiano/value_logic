# P3-01: cost quotation recoding and a fee criterion separator

Reviewer: GPT-6 Astra Pro, `/root/p301_induction_sources`.
Date: 2026-10-07 UTC. Same-model internal, nonblind mathematical review.
Scope: elementary criterion separation for the problem contract; this does not
start P3-06 or claim a new learning theorem.

**Disposition:** both proposed calculations are valid under the assumptions
below. The first is an exact change of coordinates. The second changes the
criterion and admits a market that never learns even an eventually proved
theorem. It establishes no universal impossibility of resource-aware learning.

## 1. Common portfolio contract

For each time `t`, let `p_t(phi)` be a quote in `[0,1]`. A world `W` assigns
each queried sentence a Boolean value. Let `K_n` be the specified set of worlds
used to assess the portfolio at time `n`; the intended LI comparison uses
`K_n = PC(D_n)`. The calculations below work pointwise for every Boolean `W`.

A trade is a finite position `a` in a unit security paying `W(phi)`, bought
at price `p_t(phi)`. Its assessed gain, including its cash term, is

```math
a\bigl(W(\phi)-p_t(\phi)\bigr).
```

Only finitely many trades occur before any finite assessment. Positions can
depend adaptively on available history. Fees, if introduced, are charged into
the same portfolio account when incurred. Initial wealth is a finite constant;
there are no external subsidies, rebates or interest gains included as trading
profits. The admitted strategy class and information access are fixed when
comparing criteria.

Exploitation means that all plausible wealth assessments across times have a
common finite lower bound, while their set is unbounded above. This note uses
that stated mathematical condition; it does not import a full LI theorem for a
modified objective.

## 2. Exact failure-cost quotation recoding

Define the failure-cost payoff and quote by

```math
c_\phi(W)=1-W(\phi),\qquad v_t(\phi)=1-p_t(\phi).
```

For `b=-a`,

```math
b\bigl(c_\phi(W)-v_t(\phi)\bigr)
=(-a)\bigl(p_t(\phi)-W(\phi)\bigr)
=a\bigl(W(\phi)-p_t(\phi)\bigr).
```

Sum the identity over all trades. The two portfolios have identical wealth in
every assessment world at every time. Bounded downside, unbounded upside and
constraints expressed solely through assessed wealth are therefore preserved.
The inverse transformation is the same complement/sign operation. If admissible
strategies are transported bijectively, the two non-exploitation criteria are
equivalent.

The correspondence requires the following precise qualifications:

- **Keep the worlds and change the payoff functions.** The vector
  `c_phi(W)` is not being asserted to be a Boolean truth valuation with the
  original connective operations. For example, complementing a conjunction
  changes its connective behavior. Leaving the world's meaning unchanged and
  using the explicit payoff `1-W(phi)` avoids that mistake.
- **Transport the position contract.** If arbitrary signed positions are
  admitted, the class is invariant under sign reversal. If only positive
  positions are permitted, the transformed class must permit their negative
  counterparts. Two unchanged long-only markets are not equivalent by this
  argument. Spendable-cash or asymmetric collateral requirements also need
  separate transport: equal assessed gains do not imply identical cash balances
  or identical short-selling eligibility.
- **Keep information, timing, constraints and units matched.** For the usual
  expression-based strategies, substitution `p=1-v` and coefficient negation
  preserve computability and continuity, with only elementary syntactic
  overhead. No extra theorem, label, position budget or favorable exchange rate
  is created.
- **Do not assume finite-time complement coherence.** The constructed quote
  `v_t(phi)=1-p_t(phi)` need not equal the original market's separately quoted
  `p_t(not phi)`. The new quote is a definition of the translated market.

This remains an equivalence when both accounts include the same per-unit fee,
because `|b|=|a|`. It is not a novel induction criterion merely because the
securities are named failure costs rather than truth payoffs.

## 3. A different fee-aware criterion can fail to require learning

Now change the portfolio assessment by charging `s|a|` for each unit position
traded, with `s>=1/2`. Set every quote to `p_t(phi)=1/2` at every time. For
each Boolean payoff and every signed real position,

```math
a\bigl(W(\phi)-1/2\bigr)-s|a|
\le |a|\,|W(\phi)-1/2|-s|a|
=(1/2-s)|a|\le0.
```

Every trade has nonpositive assessed gain in every world. Consequently any
adaptive finite portfolio has assessed net wealth at most its finite initial
wealth. Its plausible wealth set cannot be unbounded above. No trader can
exploit this market under the changed criterion, regardless of computation
power, even though some portfolios may have unbounded downside.

Choose a fixed consistent-theory episode in which a theorem `theta` enters
the checked deductive stream at some finite time. Its quote remains `1/2`
forever, so neither eventual probability one nor convergence to the known
Boolean answer occurs. The counterexample therefore refutes the implication

```
fee-aware non-exploitation as defined here
    => eventual correctness on every eventually proved theorem.
```

It does not refute convergence alone: the incorrect quote is already constant.
Nor does it refute every proposal to include resources in a learning system.
It shows that this particular costly-trading condition is too weak, by itself,
to force the stated truth-learning duty.

### Boundary and market-class qualifications

The constant-half quote is a computable rational **market** on all sentences.
It is not a finitely supported belief state. If the proposed criterion instead
requires finite support at every time, the exact constant-half witness is outside
its domain. One simple stronger-fee variant addresses that restriction: take
`s>=1`; then for any `[0,1]` quote,

```math
a(W(\phi)-p_t(\phi))-s|a|\le(1-s)|a|\le0.
```

For a computable enumeration of sentences, assign quote `1/2` to the first
`t` and zero to the rest at time `t`. Each pricing then has finite support and
every fixed sentence eventually remains at `1/2`. This supplies the analogous
failure witness for that domain. The variant uses the stated larger fee; it
does not silently substitute for the original `s>=1/2` example.

The half-unit threshold is also meaningful in the original witness. If a
constant fee satisfies `0<=s<1/2`, buying one share of an eventually proved
theorem each day produces upper wealth growing as `n(1/2-s)`. Before its proof
arrives, possible downside is bounded by the finitely many pre-proof
assessments; after its proof arrives all assessment worlds value the theorem
at one. Thus this elementary strategy exploits the constant-half market when
the fee is below the threshold. No general rate theorem follows from that
boundary calculation.

## 4. What the fee model does and does not represent

The fee is proportional to traded notional in a fixed unit-payoff asset basis.
It is not an independently justified model of proof-search runtime, memory,
observation expense or a flat cost of deciding to trade. A fixed one-time fee
can be overwhelmed by scaling a profitable position; the displayed per-unit
fee cannot. Bundling many unit securities into one higher-payoff security while
paying only one unit fee changes the contract. Fees that are refunded or omitted
from intermediate assessments also change it.

With nonnegative fees and an unchanged class of trades, fee-free wealth is at
least fee-inclusive wealth. Any fee-inclusive exploit is therefore a fee-free
exploit: its lower bound and unbounded upper values survive removal of fees.
So the added fees weaken non-exploitation as a requirement. The witness shows
that the weakening can remove the pressure to learn even a checked truth.

P3-01 should distinguish three obligations: recoding an existing epistemic
criterion; specifying a genuinely changed criterion; and proving whatever
truth, forecast or decision-refinement duties are claimed for that changed
criterion. The present result settles only the two elementary checks above.
Future resource-aware learning can still be investigated with explicit
additional duties and a justified resource model.

## 5. Resource record

Raw start observation: `2026-10-07T01:06:14.214570+00:00`,
`time.monotonic_ns() = 28343521719551`. Completion observation follows.
This review uses direct algebra and the stated definitions; no empirical run or
new primary-source claim is involved. Concurrent subagent elapsed time is not
added to the principal research ledger.

Raw completion observation: `2026-10-07T01:09:53.309811+00:00`,
`time.monotonic_ns() = 28562616952647`. Observed review-session elapsed:
`219.095233096` seconds. This is not additive phase ledger credit.
Token and billed resource totals are unavailable.
