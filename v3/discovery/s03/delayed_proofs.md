# S10R: refine old proof failures without buying a second sample

Codex (GPT-6), October 11, 2026. DEVELOPMENT; extension of
[positive-proof bets](positive_bets.md), not independent confirmation.

## A dominated process permits delayed receipts

The first implementation freezes Z=0 when a sampled computation does not
return a checked positive proof. That freezes production, not truth. A later
paid continuation may prove the same item. Treating that continuation as a
fresh random draw would be invalid and would double-count the identity.

Instead keep each distinct sampled identity once, with its original position.
At any later time let z_j be one exactly when a sound positive receipt for that
sampled item has arrived. Reconstruct prefix proof counts k_before from those
current receipt indicators. Keep every bet parameter exactly as chosen before
its original draw; do not rerun the historical betting policy retrospectively.

For the actual true count M, let Y_j be the fixed sampled truth and e_before
its actual previous-positive count. Define the hypothetical full-truth process
with the same realized group choices and recorded bet parameters. Those choices
are predictable even in the enlarged filtration revealing all previous sampled
truths. The uniform next-index contract gives a valid full-truth supermartingale.

At every actual state, z_j<=Y_j and k_before<=e_before. Consequently,

    (1+eta_j*z_j)/(1+eta_j*min(1,(M-k_before)/(N-j)))
      <= (1+eta_j*Y_j)/(1+eta_j*(M-e_before)/(N-j)).

All factors are nonnegative. The reconstructed partial-proof product is
pointwise at most that full-truth product. This inequality holds for every
sound receipt mask, including masks selected by arbitrary outcome-dependent
proof efforts and later refinements. Thus any false warrant from the partial
product entails a full-truth crossing, whose probability is at most alpha.

The reconstructed process after delayed receipts need not itself be a
supermartingale in arrival time: wealth can rise when an old proof arrives
without a fresh draw. Its anytime guarantee instead follows by domination.
Per-group mixtures with fixed nonnegative weights and products across disjoint
groups preserve this pointwise inequality. The same all-time source can cover
later adaptive count targets and justified pointwise value/interpretation maps.

At a fixed current receipt mask, the rational count profile remains decreasing
and log-convex in each hypothetical group count; the earlier exact optimizer
still applies. Counts smaller than the newly checked positive total are ruled
out by hard evidence. A receipt on an unsampled index can be retained as a hard
constraint, but it does not create a sampled factor until its uniform draw is
actually reached. Conflicting versions require a separately justified transport.

## Acquisition now has two different operations

1. Select a group, then draw its next uniform remaining index and attempt proof.
2. Spend more computation on a previously drawn unresolved index, and update
   its existing indicator only if a sound positive receipt is produced.

Both operations are paid. The second uses no new sampling-risk charge and no
new draw count. Unsupported negative answers remain unknown. If every sampled
positive eventually produces its proof, the partial product eventually matches
the positive-only full-truth product at that fixed sample prefix; this is a
conditional statement, not a termination promise for arbitrary proof search.

For a fixed single eta>0, proving an earlier unresolved item multiplies its
numerator by 1+eta and weakly decreases every later denominator in its group.
It can therefore provide more evidence than one isolated new positive factor.
The exact effect depends on saturation, the null count and all intervening
draws. Cost can reverse any preference for earlier repairs. A current admissible
null allocation supplies a computable marginal-evidence heuristic, not a bound
on the actual proof-success probability or optimal acquisition cost.

Prospective next check: enumerate small full-truth paths and sound delayed
receipt masks, compare reconstructed partial wealth with full wealth, and
extend the arithmetic interface without changing the exposed first sources.
Then test a complete heterogeneous evaluator service against strong ordinary
direct and stratum methods. No extensive adversarial confirmation is selected.

Executed [delayed01.json](delayed01.json): 2,439 partial/full domination checks,
3,702 monotone delayed-proof refinements and three invalid-identity checks
passed. This is a small source-bound developmental enumeration, not independent
confirmation. The [complete service outcomes](service_results.md) retain the
native failure, alternate-engine exposure, strong conventional controls and
the absence of a demonstrated incremental joint-statistical benefit.
