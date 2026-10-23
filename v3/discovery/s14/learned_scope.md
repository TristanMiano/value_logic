# Let partial evidence choose how broadly a fallible model may be used

Codex (GPT-6), DEVELOPMENT, October23,2026 UTC. A constructive composition
of target_warrants.md, hidden_rank.md and sequential_rank.md. All source
features, model equations and receipt prices are fixed before sampling.

Let H have the fixed prior model equations as independent rows. A dual
equation h=a*H is represented by coefficient vector a in syndrome space.
Paid partial training evidence supplies S_hat=span(union_i Z_i), and the
retained coefficient space is E=S_hat-perp. After the sequential rank test
accepts, the common event z_new in S_hat has probability at least1-epsilon,
with training confidence at least1-delta.

For every target/budget interface(T,B), let D_(B,T) be the exact span of
eligible dual CIRCUITS from target_warrants.md. If its coefficient space
is contained in E, the original model's ENTIRE legal interface is safe on
the same common event. This includes choosing T and B after inspecting
the partial training evidence and later adapting receipt/target choices
within each deployment case. No separate penalty is needed per circuit,
target or budget because all selected equations hold on one source event.

Do not merely check that SOME equations survive and then permit every
old model inference. The required inclusion of D_(B,T) in E is substantive.
Consistency of the model with each case's actual receipts remains required.

## A compact all-budget implementation for graph models

Use the earlier polynomial rooted-cycle-basis compiler for a fixed target
set T. It produces a list of independent cycles h_j, with prices b_j,
whose price<=B portion spans D_(B,T) for EVERY B. Write h_j=a_j*H.
With a basis s_1,...,s_d of S_hat, test a_j*s_l=0 for all l.

Define b_bad as the least price of a failed test, or infinity if none fail.
Every budget B<b_bad is certified; if b_bad is finite, budget B>=b_bad
cannot be certified from this S_hat through the exact task-source theorem.
The strict endpoint matters because cycles with price EQUAL to B are legal.
For an arbitrary finite allowed budget menu, choose its greatest member
strictly below b_bad. At equal prices check the entire tied batch.

This requires O(q*d) binary inner products after compilation, where q is
the retained basis-list length. The cost of preparing that list, acquiring
S_hat and performing the products remains charged. For different target
sets one can use separately prepared lists, all expressed in the SAME
fixed feature space; no free compilation is assumed.

Nested refinements shrink S_hat and can only increase b_bad for a fixed
cohort. Thus paid evidence can simultaneously increase the range of
authorized inferences and improve the hidden-rank confidence certificate.
New cases can expand S_hat and withdraw previously permitted budgets.
This is an ordinary linear-algebra implementation of an exact scope rule,
not a new cycle-basis algorithm or a measured economic advantage.

## One certificate can protect later learned models jointly

There is a stronger consequence of the sequential test than separate
per-time risk bounds. Let tau be its FIRST acceptance, and denote the
unobserved actual sample span there by S_tau. Except on the delta event,
its population missing mass is<=epsilon. Every later truthful outer span
S_hat_t that still contains all tau latent training vectors contains S_tau.
Consequently ALL later retained rules, even their jointly selected span,
hold on S_tau. A fresh case in S_tau is protected across every such later
model and scope revision, not merely one model at a time.

The test need not cross its threshold again to retain this common-event
guarantee. Continuing to sample can make a fresh test statistic fall, but
cannot change the already certified population missing mass of S_tau.
Future receipt refinement and additional cases preserve containment as
long as the original cohort and fixed feature map remain represented.
Discarding cases, changing feature maps or accepting non-truthful receipts
can destroy the invariant and requires a new argument.

This also clarifies the earlier fixed-N result: once a PREDECLARED cohort's
latent-span event is valid, truthful later extensions containing that
cohort are covered. The sequential construction is needed to choose the
FIRST certification sample size adaptively, not to charge repeatedly for
an already established event.

The coverage is per new iid case. It does not imply no errors across an
unbounded future stream, or a conditional error rate among rare releases.
The same ordinary statistical/linear-algebra pipeline ties. The possible
contribution is this explicit partial-evidence, changing-scope contract
and its certificates; closest-prior novelty and complete costs remain open.

## A small scope-expansion example

Take three disjoint triangles, with a vertex-XOR model on their nine edges.
One edge in each triangle is an allowed target. Price the two other edges
at1,2,3 respectively within the three triangles, giving cycle receipt
prices2,4,6. The three cycle parities are the fixed syndrome coordinates.

In a200-case cohort, suppose197 syndromes are certified zero and three
are initially completely unresolved in F2^3. The latent rank is at most3,
even though those cases are not completed. At epsilon=delta=1/20 the
sequential acceptance condition is(39/38)^197>=160, which holds. The
initial outer span is all of F2^3, so it supplies no nontrivial equation
and cannot yet authorize any triangle prediction.

Now buy truthful refinements showing all three unresolved syndromes equal
(0,0,1). The outer span shrinks to that line and k_bar becomes1. The first
two cycle rules become available, while the third may still fail. The
least unprotected price rises from2 to6. On an integer budget menu0..6,
the maximal certified budget rises from1 to5, now permitting useful
predictions on the first two targets. The already established sequential
event covers the refinement; no new cohort or per-rule confidence charge
is required. The updated fixed-N numerical bound is a separately calibrated
alternative, not automatically a second free confidence event.

All197 zero certificates and all three refinements have acquisition costs.
This is a coherent possible receipt state, not a simulated frequency result
or a claim that this particular source makes the full model always false.
