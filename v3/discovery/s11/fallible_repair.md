# A fallible source does not become a theorem after conditioning

Codex (GPT-6), DEVELOPMENT. This inexpensive derivation connects the repair
candidate to the original fallible-model question. It is a conventional
coverage argument and a selection counterexample, not a new general learning
theorem. No data were acquired to establish the coverage premise.

## One globally warranted source

Let X be the original assignment on a fresh task and F a fixed model support.
Assume a warranted bound P(X not in F)<=epsilon. A randomized controller
inspects original bits, then either abstains or releases X xor b. For every
reachable history h with F_h nonempty, require every mask in its randomized
support to map ALL of F_h into the fixed target G. On F_h empty, abstain.
Then, for every original X in F and every private seed, any released vector
belongs to G. Consequently

```math
\Pr\{\text{release violates }G\}\le\Pr\{X\notin F\}\le\epsilon.
```

There is no factor for the number of queries, leaves or intermediate
certificates: every such certificate follows from the SAME globally valid
event. This is an unconditional guarantee. Conditional risk at a rare receipt
can be as large as min(1,epsilon/P(h)); no epsilon-conditional guarantee follows.
If F was fitted on prior data, require its coverage statement conditional on
that fitting information, or a valid uniform statement for its selection rule.
If that statement itself holds with confidence 1-delta, preserve both levels;
the joint failure bound is at most epsilon+delta, with no claim that either
quantity has been measured in this session.

The event X in F means truth of the supplied model on the task. It does not
mean validity of a checked proof. A checked derivation from a false premise
does not warrant that premise. If the task is one fixed mathematical object,
the source of the probability must be specified rather than invented.

## Selection can destroy a per-model promise

Take M equally likely original labels. Model j excludes just label j, so every
fixed model has error 1/M. If the controller learns the label and selects the
model that excludes it, the selected source is false with probability one.
Thus replacing F at each history by whichever convenient fallible model has
the desired conclusion is unsound. A simultaneous guarantee, a bound on the
union of failure events, or an independently justified selection-aware risk
bound is needed. Model multiplicity is not a source of extra truth.

If a fixed library has joint validity event of probability >=1-epsilon,
arbitrary adaptive selection within that library is covered by the same event.
If only individual errors epsilon_j are justified, the elementary bound is
sum_j epsilon_j, truncated at one. Independence is not presumed. This contrasts
with independent confidence-tail checks on reused, selected receipts.

## Safety and usefulness remain different

Abstention is always safe under this contract, so the preceding inequality
alone is not a useful-positive-result claim. Query/edit fees and achieved
terminal cost must accompany it. The existing exact repair LP assumes F is
true for its objective; the coverage bound does not automatically transport
its regret optimum to misspecified tasks. In particular, a newly enlarged
comparator class can change regret even when the controller's absolute cost
does not change. [The refinement counterexample](repair_geometry.md) already
shows that danger.

If a fixed, fully specified controller and a fixed benchmark have bounded
pointwise cost gap g on a larger universe U, one can separately optimize
the gap over laws with P(F)>=1-epsilon. Put a=max_F g and b=max_U g. Since
b>=a, the exact value is (1-epsilon)*a+epsilon*b: every admissible law is
bounded by this value, and a mixture of maximizing assignments attains it.
When b=a, use a point mass in F. This elementary contamination formula is
only for a fixed pointwise benchmark. Worst-law regret against a law-optimal
policy is a different expression and cannot substitute this formula without
an additional reduction. Off-source release cost, penalties, fallback and
the benchmark must all be defined before claiming a robust improvement.

The immediate research disposition is to retain the safety adapter and reject
automatic robustness of the regret percentages. Obtaining economical,
selection-valid coverage is a separate candidate; no extra calibration sweep
is warranted until its acquisition interface and useful delta are explicit.
