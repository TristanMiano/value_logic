# Action-adaptive graph audit service: observed scope

**DEVELOPMENT — Codex (GPT-6), October 14, 2026 UTC.**

The [derivation](action_audits.md) connects the exact remaining minimax regret
to maximum cut of the unaudited induced graph. On a forest this is the sum of
the remaining edge weights, so the observation task becomes ordinary weighted
partial vertex cover. The optimal sufficient-set cost is independent of audit
outcomes. This is a useful exact acquisition consequence in the stated source,
not a novel vertex-cover solver or a promotion result.

The command `python v3/discovery/s08/action_audits.py v3/discovery/s08/aa01`
completed 26 graph/tolerance conditions. Twelve small trees have n=2..7 and
all bit outcomes; two large trees have n=32/128 and eight bit outcomes per
tolerance. [Design](aa01/design.json), [source](aa01/impl.py) and
[results](aa01/results.json) are preserved with plans, physical receipt
prefixes, outputs and post-output diagnostics. All 1,028 outputs per arm
passed original-clause and local regret checks. Small-case sufficient-set fees
also agreed with exhaustive subset search, and every emitted small-case bound
equaled a post-output exhaustive compatible-source maximum.

| Arm | Outputs | Physical audits | Base audit fee | Setup named units | Service named units |
|---|---:|---:|---:|---:|---:|
| Residual-weight DP | 1,028 | 2,852 | 7,148 | 340,336 | 370,560 |
| Ordinary cost-axis DP | 1,028 | 2,884 | 7,148 | 3,717,303 | 370,944 |
| Greedy coverage/fee | 1,028 | 3,348 | 7,796 | 5,410,571 | 376,512 |
| Full identification | 1,028 | 8,672 | 26,532 | 22,355 | 440,400 |

The exact planners agree on **fees**, not necessarily audit counts: tied
optimal sets can contain different numbers of differently priced vertices.
Their computed actions can also incur different actual regret within the
same requested tolerance. Full identification's exact outputs need not be
paid for when tolerance is positive, but its very low preparation cost matters
at short reuse horizons. The greedy implementation rescans every edge per
candidate vertex; its large bill is not a credible lower bound on efficient
ordinary greedy coverage.

The residual-axis recurrence is itself an ordinary graph algorithm. An
ordinary controller given that recurrence and the same source ties its
capability and can share its implementation. The cost-axis gap therefore
cannot establish a new mechanism's advantage over the strongest specified
ordinary control. It illustrates how an inappropriate DP dimension can waste
work. Four controls rejected an extra hard clause, a negative scale, a cyclic
source and an insufficient audit plan.

Named units are not a complete monetary bill. Source validation is allocated
once to each arm; the implementation additionally calls its admission helper
inside the two exact planner functions, an implementation overhead requiring
separate attribution in a full bill. Provider/hash/export work is not fully
priced by the named arithmetic counts. Exact serialized trace bytes are
retained in the result. Whole-development CPU/wall measurements include
exhaustive diagnostics and cannot be described as isolated service timings.

The conditional remaining-information theorem is more useful than a claim
about this prototype's wall speed. Next check its lower bound independently,
and examine sources where the binary endpoint rule fails. In particular,
continuous or multi-level costs and extra feasible-action constraints require
different acquisition policies; the present theorem does not transfer merely
because the source still has a graph representation.
