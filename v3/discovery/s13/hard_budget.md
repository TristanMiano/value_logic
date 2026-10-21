# Expected acquisition budgets do not imply hard-budget replacement

Codex (GPT-6), DEVELOPMENT, October21,2026. A two-bit counterexample to an
overextension of experiment_frontier.md, using an ordinary adaptive stop.

Take n=H=2, unit query fees, no reset fee and two fair bits. A cap-two
informative invoice reads one bit: stop at count1 for0 and use the other
coordinate as a discarded marker at count2 for1. The inherited hard-price
bound for exact parity is4. Every always-correct decoder has some world
whose bill is at least4; free randomized tapes do not reduce that pathwise
maximum.

Nevertheless a hard budget3 permits a useful partial experiment. First read
x1 through this encoding. If its invoice is2, stop without a parity answer.
If its invoice is1, read x2 through another cap-two episode, using x1 as the
distinct marker if needed. Return the now known parity. The four equally
likely worlds have bills2,3,2,2 (order00,01,10,11), and the expected bill is9/4.
The reveal event x1=0 has probability1/2 conditional on either parity, so the
retained output is exactly an erasure experiment E_(1/2).

No policy that first flips an independent coin and then, on a positive-probability
branch, runs an always-correct full decoder can achieve this under the same
hard budget3: that branch retains the decoder's at-least4 worst bill. Thus
the convenient *implementation* in the expected-budget frontier does not
transport to a hard budget, even though the information comparison between
binary experiments still holds. The successful partial procedure itself is
an early-abstaining decoder, not an exact decoder selected before purchase.

This also exposes why a generic claim that partial computation is wasteful
would be wrong. A task with a hard deadline may value certified answers on
some branches when a complete all-branch service is unaffordable. Further
development should price this different service explicitly instead of
reusing the average-budget theorem. No new optimality claim for partial
hard-budget experiments is made by this example.
