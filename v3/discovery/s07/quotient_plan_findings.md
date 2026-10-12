# Conditional complete audit planning from source geometry

**DEVELOPMENT — ChatGPT (GPT-6 Astra Pro), October 12, 2026 UTC.**

[quotient_plan.py](quotient_plan.py) implements the complete count-state
recursion in [quotient audits, Section 6](quotient_audits.md). This is a
conditional planning component. It does not itself acquire the required
logical proof, admit a real source, make an observation, or return an
original-source checked repair. Those interfaces and bills remain necessary
for an integrated service. The [saved result](quotient_plan_results.json)
contains no new acquisitions.

## What the count state preserves

The source has n independent mandatory costs, each a or 2a, plus one unknown
decision bit choosing which of two symmetric repairs incurs an extra H.
A separately checked fixed repair block has exact cost C. The source proof
must warrant the mandatory/equal-choice geometry. Replacement costs p and
the tolerance is strictly below H, so a repair leaf needs to know the
decision bit.

After k mandatory observations, h of them high, the compatible total mandatory
cost is between `na+ah` and `na+a(h+n-k)`. Row identity and observation
history do not further affect the conditional quote because supports and
observation tariffs are identical and independent. The state keeps only
(k,h), while a future executing service must retain the actual row receipts.

Replacement terminates when its worst regret is within tolerance. A repair
leaf buys the decision audit when its worst comparison with replacement is
within tolerance. Otherwise the next mandatory audit has both children in
the quote, and their maximum determines its worst tariff. The implementation
uses memoization and stops expanding a state when a zero-cost terminal is
available or when a sufficient decision audit costs no more than any
mandatory observation could cost. This pruning follows from nonnegative
future tariffs; it does not use hidden outcomes.

The largest possible state set has `(n+1)(n+2)/2` entries. Construction
arithmetic, state storage and comparison operations are counted separately
from the observation tariff. Exact rational values are used; the operation
count does not assert constant bit complexity or a wall-time deadline.

## Independent small comparison

The diagnostic uses a different full state: every mandatory feature is
unobserved, low or high, and the decision bit may also be unobserved or known.
It directly checks the worst regret of replacement and both repairs over all
compatible hidden configurations. It permits **every unobserved coordinate**
and an **early decision audit** at each nonterminal state, with no count-state
symmetry or delayed-bit premise supplied to it.

All **135** comparisons match the compressed quote exactly. They cover n from
0 through 4, tolerances 0, 1/2 and 1, three relative observation tariffs and
low, middle and high replacement prices. The finite enumeration is validation
only; it does not supply inputs or optima to the compressed planner. This
comparison checks the specific complete recursion and pruning. Its general
scope remains the proof in the quotient note, not extrapolation from tests.

## Larger conditional examples

The recorded examples use a=2, H=8, C=2, tolerance 1, and unit observation
tariffs. These are fixed numerical planning inputs, not measured source
outcomes or deployed prices.

| Mandatory features n | Replacement price p | Worst quoted audit tariff | Compiled count states | Named planning units | Full identification tariff |
|---:|---:|---:|---:|---:|---:|
| 8 | 18 | 0 | 1 | 28 | 9 |
| 8 | 26 | 8 | 24 | 732 | 9 |
| 8 | 35 | 1 | 1 | 31 | 9 |
| 32 | 66 | 0 | 1 | 28 | 33 |
| 32 | 98 | 32 | 288 | 8,880 | 33 |
| 32 | 131 | 1 | 1 | 31 | 33 |
| 128 | 258 | 0 | 1 | 28 | 129 |
| 128 | 386 | 128 | 4,224 | 130,752 | 129 |
| 128 | 515 | 1 | 1 | 31 | 129 |

The low-price case can choose replacement without knowing the decision bit.
The high-price case needs only that bit; it can ignore all mandatory costs
after their logical role is proved. In the middle case, most mandatory costs
really matter to replacement, and the planner saves only one observation
relative to full identification. The 512-feature accepted input boundary was
also checked separately during development: its middle quote is 512 and uses
66,048 count states. That boundary check is not included among the 135 saved
small comparisons or treated as another acquisition run.

## The full-cost consequence remains conditional

The middle 128-feature example spends 130,752 named planning operations to save one
unit-priced observation relative to full identification, before proof,
admission and execution costs. It therefore illustrates why an inexpensive
state representation can still be too costly for its decision benefit. A
monetary claim needs the actual conversion and the complete baseline bill.

The far-price cases permit large observation reductions, but their ordinary
comparison is strong: simple source-aware bounds also recognize the free
replacement or one-bit repair decision. An ordinary controller given the
same geometry, source, tariffs and proof bank can use this exact count
recursion. Full latent identification is an illustrative control; a win
over it does not establish a win over ordinary decision reasoning.

The next integration should first acquire and check the source geometry,
then include these quote costs in its acquisition choice. It must support
the actual observation source, select a compatible fixed repair at a leaf,
recheck its original logical feasibility and regret bound, and retain every
paid or unresolved prefix. The signed geometry prototype supplies a separate
route toward that first premise; neither component silently completes the
other's contract.
