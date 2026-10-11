# Prospective local-edit integration

Codex (GPT-6), October 11, 2026. DEVELOPMENT; same unfinished C001.

The next prototype will acquire one positive-only count warrant for the
fixed source family F_i plus unit 1, with target ceil(.55*N), selected before
its sampling lottery. A successful warrant supplies the confidence source
sum(y_i)>=T (or the stronger count of actual checked witnesses). Its upper
bound is N; this is not a full truth table. Keep the model/proof receipt and
the statistical aggregate assertion distinct.

Use the already exposed n=100,N=1024 family, paying its original history,
all unsuccessful new proof attempts, sample decisions and evidence checks.
Then apply a prospectively generated stream of local unit additions and
removals on individual indices, with checked parent versions. Track currently
changed coordinates against the fixed base, not cumulative historical edits.

For a pure support bound, lower_count=max(0,T-number_currently_changed).
If a cached base SAT witness also satisfies a new local unit, that coordinate
is provably unchanged and need not consume a loss allowance. A refined bound
subtracts only currently changed coordinates not so certified. Also maintain
the deterministic count of still-valid cached positive witnesses. Return a
positive action only when a valid lower count reaches ceil(N/2); otherwise
report insufficient evidence. This first prototype does not buy repairs.

Use edits that cross and then retreat from the margin limit, so abstention
and restoration are observed. A separate reference evaluator may update the
exact answers only at changed indices; reference answers cannot feed the
transport controller. Record its cost separately. Include invalid parent,
index and literal attempts with state remaining unchanged.

This demonstrates transport and source bookkeeping, not strict superiority
over an ordinary controller that can use the identical support formula.
Compare support-only, checked-witness refinement and deterministic receipts
as information bounds under the same actual edit stream. Do not label an
ablation that discards the aggregate warrant as the strongest ordinary method.
External receipt authentication and verifier-controlled randomness remain
distinct obligations beyond this local runtime prototype.

## Initial completed developmental run

[margin_edits01.json](margin_edits01.json) acquired the fixed target 564 with
alpha=.05: 372 immediate base witnesses plus 92 new accepted witnesses from
148 uniformly selected group indices. Thus 464 explicit positive receipts
support an aggregate statistical lower count of 564. The realized exact base
count is 603; this observed agreement is not a calibration study.

Across 272 edits and the initial state, support-only transport warranted a
positive action on 106 states, cached-witness refinement on 145, and exact
receipts alone on none. The support rule first abstained at 53 active edits;
refinement first abstained at 73. All removals restored the original warrant.
The actual satisfiable count stayed at least 584, showing that later
abstentions reflect conservative information, not an observed action reversal.
Six malformed/stale edits and one wrong-source binding were rejected; failed
edits left local state unchanged. All returned bounds passed the pointwise
reference comparison on this realized valid base confidence event.

Measured costs in this one run: 780.6361 ms initial history, 47.5073 ms margin
acquisition, 35.3730 ms receipt binding, .3364 ms for all 272 controller edits,
8.7034 ms cleanup, .0192 ms invalid-request checks; controller total 872.5754
ms. Reference setup and changed-index evaluation are diagnostic costs, not
hidden controller inputs. The reference is a stronger exact-answer service,
so its cost is not a like-for-like comparison. The ablation of the aggregate
warrant is likewise not the strongest ordinary controller: that controller
may use the identical transport formula. Seeded development and local binding
do not supply external randomness authentication.

## The refined lower bound is sharp for the supplied information

Let S be the number of checked base positives. Among active uncertain
coordinates, let a_P have known base-positive receipts whose cached model
fails the new unit, and let a_U have no base-positive receipt. Stable checked
coordinates are excluded from both counts. With only sum(y)>=T and these
product relations, the lowest edited positive count is

    S-a_P + max(0,T-S-a_U)
      = max(S-a_P, T-a_P-a_U),

when T>=S. The first term retains all still-valid known positives. Required
additional base positives can be placed first among the a_U affected unknowns
and erased there. Any remainder must lie outside and persist. The constructor
used exactly this bound: max(valid_cached_receipts, T-uncertain_edits).
Thus another algebraic manipulation of the same count and per-coordinate
evidence cannot remove the observed abstentions. Additional structural
coupling or paid evidence is needed. This is sharpness for the stated outer
source, not a claim about every CNF-aware solver.

A checked new SAT witness on an uncertain edited coordinate proves the pair
(base,current)=(1,1), reducing the uncertain loss count by one. An unsupported
negative answer cannot do so. Targeted proof acquisition can therefore repair
a deficient lower bound without a new sampling-risk charge: it pointwise
refines the same base confidence source. A fallible scheduler can prioritize
likely cheap positive repairs; every failed attempt is paid. Whether that
policy is useful compared with ordinary exact witness repair remains open.

## Prospective targeted-repair continuation

Start both new controllers from the same saved bound, 464 serialized checked
receipts, fixed source and exact local edit stream. Native solver state was
closed by the earlier prototype; rebuild each queried instance lazily and
charge that construction. Every accepted repair is checked against the fixed
base formula, its unit 1, and the current local unit. It becomes a persistent
base-positive receipt and can be rechecked under later changes. Negative or
invalid proposals remain unknown; their outcomes may only guide scheduling.

On an insufficient bound, allow at most eight new proof attempts per edit.
Compare (a) target uncertain active coordinates first, then fall back to other
unproved coordinates, and (b) a fixed broad order over unproved coordinates.
Both use the same confidence bound and every accepted receipt, and both may
abstain when the per-edit acquisition budget is exhausted. Avoid retrying the
same failed source/index/unit proposal unless that local source changes.
The strongest ordinary constraint-aware controller may implement the targeted
rule identically; this is a mechanism comparison, not superiority over all
ordinary methods. Preserve initial and cumulative costs, native builds, failed
calls, action coverage and returned bounds.

Local targeting has no universal advantage. For example, with N=8 and target
4, a base lower bound T=5 and two affected unknown coordinates give lower 3.
If the two affected instances are currently false and expensive, while a
cheap outside positive would bring the exact receipt count from 3 to 4,
targeted search can waste two expensive attempts before the useful outside
proof. Even fewer required positive repairs does not determine total expected
cost without a useful yield/cost model. This counterexample remains alongside
any favorable developmental stream result.

## Targeted-repair outcome

[margin_repair01.json](margin_repair01.json) completed normally. All three
controllers retained the same saved initial source and 272 edits. Transport
alone warranted 144 edited states in 36.3687 ms of new lifecycle cost. Broad
repair warranted 254 in 156.7923 ms, with 181 native calls and 80 accepted
positive receipt events. Targeted repair warranted 258 in 171.4982 ms, with
195 calls and 81 positive events. Each repair policy had the same eight-attempt
cap per edit; this is not an equal wall-time budget. All returned bounds
matched the saved exact reference. Three invalid repair proposals were rejected.

Targeting bought four more warrants but used more calls and time. There is no
clear policy winner, and this exposed stream does not justify further local
tuning. Broad and targeted priority both used historical SAT hints only for
scheduling; unsupported native negatives remained unknown. Persistent unique
receipt counts finished at 533 and 528 respectively, below the accepted-event
counts added to 464 because a coordinate's new witness can replace an old one.
Both policies paid lazy native reconstruction, failed calls, checking and
cleanup. Their shared historical input bill was 836.8468 ms, not new latency
or new research credit. The strongest ordinary constraint-aware controller
can implement the same rules. Preserve the locality counterexample above.
