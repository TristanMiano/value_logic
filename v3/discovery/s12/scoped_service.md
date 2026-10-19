# A bounded service for task-scoped reliance on fallible models

Codex (GPT-6), October 19, 2026. DEVELOPMENT synthesis of constructions,
not a frozen confirmation candidate or an application performance claim.
This is a possible useful contribution under the author's clarified standard.

## Contract

There are n fixed original Boolean facts x, m current registers, and M supplied
satisfiable binary source models F_j. The models can disagree and can all be
globally false of actual x. Each current register is a constant or a copy/
complement of one original fact. Allowed changes have exact deterministic
semantics and update those lineage records; observations of current registers
are exact and their physical access fees are charged.

Before deployment, declare Q, the possible original origins of observations,
and a family J of possible original scopes of binary target clauses after
lineage substitution. Repeated origins use singleton scopes; constants need
no source bit. No new origin may silently enter this contract. For each model,
let H_j be its task envelope from [task_adequacy.md](task_adequacy.md).
The coverage premise is the ONE event

    actual original x belongs to at least one H_j.

It need not say that x belongs to any F_j. A justified probability at least
1-epsilon for this event gives the statistical version; a checked deterministic
premise gives exact conditional validity. Where the premise comes from and
what it costs are distinct from the algorithm below.

## Mechanism and guarantee

Prepare each F_j's forced literals and the original local projections that
the allowed target scopes require. Translate observations back through current
lineages into units about Q. Maintain separate propagation states for the M
models, rejecting a branch only if its receipt is inconsistent. Keep a shared
lineage map, since actions have one actual semantics independent of model j.

At any proposed release, substitute the proposed current lineage into the
target clauses. Compute each needed original pair/singleton projection in
every retained branch by the binary receipt rule. Take their union, map tuples
through constants/complements, and check that every resulting target pattern
satisfies its clause. For a next coordinatewise unary-map menu, the existing
compiler describes every permitted map using two truth-table bits per register;
binary target clauses yield binary clauses on these map bits. Extra legal-action
constraints and utility optimization must be accounted for separately.

A particular proposed copy can be checked by its substituted lineage. Choosing
which source register to copy from an arbitrary menu is a different optimization
problem; no general compact 2-SAT encoding for that menu is asserted.

On the coverage event, choose one adequate j. Every actual receipt on Q remains
compatible with F_j: its H_j witness agrees with all observed origins. At every
target scope, the actual original pattern remains in F_j's conditional
projection. Thus this branch is never wrongly discarded, and a release valid
for the union is valid on the actual current state. Induct over the observation/
action history. This proves simultaneous correctness for every released target
along any finite or indefinitely continuing adaptive stream within the contract.

Consequently, in the probabilistic version, the event that ANY such release is
wrong is contained in the initial coverage-failure event and has probability at
most epsilon. This is unconditional. It is not a conditional-error guarantee
among rare released cases, and it does not cover faulty actuators, noisy
observations, semantics changes or a newly introduced model/interface.

## Charged work and limitations

For one fixed binary model, after initial preparation, the bookkeeping from
[lineage.md](lineage.md) is O(n+m+|F_j|+U+R+sum_t |G_t|), plus first-use pair
preparation. Sharing lineage updates across models gives the corresponding
bound O(m+U+M*(n+R+sum_t |G_t|)+sum_j |F_j|), plus all initial and first-use
preparation. This counts submitted observation records even when repeated.
Each new forced literal/outgoing implication is processed once per branch.
Contradicted branches can be retired. Forked histories have separate budgets.

Physical observation/write fees, source production, adequacy certification or
calibration, storage, proof checking and action optimization remain outside
this bookkeeping term and must enter any complete-cost comparison. Querying a
current constant is not a way to recover the overwritten original value.
Adding relational receipts, including many invoice observations, is not a unit
update and needs new source inference. Positive-slack weighted repair sources
also lose the binary receipt shortcut.

## A nonvacuous three-fact use

Take F=(q=>z) AND (z=>a). Allow observations of q and targets on registers
whose origins are a. H is q=>a. Actual (q,z,a)=(1,0,1) makes F false but H true.
Copy a into a new register r, observe q=1, then toggle r with target NOT r.
The service certifies the toggle and the actual target holds; a remains
unobserved and unchanged. A full-model truth requirement would reject this
actual world. Allowing observations of z would require a stronger contract,
so the same adequacy certificate must not be carried into that interface.

This is a capability delta over demanding global model validity and over
recomputing every current-world set. It is not a performance advantage over
ordinary forgetting, symbolic regression and cached binary inference given
the same contract; that realization is identical and ties. The individual
machinery is established. The contribution still to assess is the explicit
composition, its weak reliance condition, the paid stream bound and the
boundaries needed to use it correctly.

The component finite screens pass, but this complete service has not received
an independent reconstruction or a deployment workload. Do not convert the
component counts into a complete-service test count. A next useful step would
select a naturally occurring duty, check the closest implementation literature,
and decide whether the source/preparation and adequacy bill can be amortized.
If that fails, retain the mathematical adapter and return to broad discovery;
do not make this one service the whole program.

## Late strengthening of the adequacy premise

[union_adequacy.md](union_adequacy.md) replaces the sufficient union of
individual envelopes above by the potentially larger envelope of the model
union. Different target scopes can have different branch witnesses agreeing
with all permitted observations. The branch-aware algorithm and charged work
bound are unchanged; the new witness proof establishes the weaker premise.
The same note gives a strong per-task model-selection comparison, so no
ensemble advantage is inferred from marginal error bounds alone.

[temporal_adequacy.md](temporal_adequacy.md) and
[observable_adequacy.md](observable_adequacy.md) are separate extensions with
their stated representation and public-observation contracts. Their semantic
proofs do not count as an end-to-end implementation of this binary service.
