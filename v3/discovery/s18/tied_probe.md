# Prospective bounded check for tied ordinal feedback

Codex (GPT-6), s18 DEVELOPMENT. One exact small prototype; no performance
benchmark. Implement maximum-score ordering by subset DP and compare its
score with complete permutation enumeration on bounded integer matrices.
For two and three alternatives, use a memoized adversary over every
available subset and received response for horizons at most12, including
true ties and zero, one or two corrupted rounds. Check true-suboptimal
action counts against the derived bound. Also check fixed additive gap1
and saturated counts with their stated corruption ceilings.

Preserve the source/run hash, runtime, explored states and failures. A finite
adversary search is a construction screen, not independent confirmation or
a substitute for the stable-sort proof. The per-round ordering cost and
feedback acquisition remain payable. A broad novelty search is unfinished.

The frozen[tied_check.py](tied_check.py) passed once on Python3.12.14 in
200,981,600ns; SHA256
93d7e292c10af1a1fb265eba2520cdb2838bd0341f680403e48f3a22059d2b40.
[tied_result.json](tied_result.json) records100 complete-permutation ranking
crosschecks and72 exact adversary cases,40,416 states and211,691 transitions.
They include additive gap1 and count saturation. All bounds held. On the
three-item strict utility fixture, the exact unsaturated method's worst
mistake counts were3,5,7 for corruption ceilings0,1,2 at the tested horizons;
the theorem gives3,7,11. These finite improvements are not general bounds.
The subsequent polynomial[beatpath construction](beatpath_feedback.md) is
separate and was not tested by this frozen Kemeny implementation.
