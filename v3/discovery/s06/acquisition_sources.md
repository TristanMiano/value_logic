# Existing regret elicitation and the joined evidence purchase

Contributor: **ChatGPT (GPT-6 Astra Pro)**. October 12, 2026 UTC.
DEVELOPMENT primary-source bridge; no new novelty or performance verdict.

## Closest direct elicitation comparison

Boutilier, Patrascu, Poupart and Schuurmans (2006), *Constraint-based
Optimization and Utility Elicitation using the Minimax Decision Criterion*.
[Author preprint](https://www.cs.toronto.edu/~cebly/Papers/BPPS-aij06.pdf),
Sections 3, 4.2 and 5.2–5.4; especially PDF pp. 20–21 and 32–35.
Read its regret definitions, anytime constraint generation, retained constraints,
and largest-gap/current-solution query rules. This is a close conventional
comparison: feasible configurations, uncertain utility parameters, regret-based
elicitation and computational reuse already belong to that method. Its current
solution rule targets parameters in a current solution/adversarial alternative;
its largest-gap rule reduces parameter uncertainty more uniformly. It also
allows early optimization stopping with separate regret bounds. Neither this
paper nor the new s06 fixture grants a calibrated distribution for future
solver work. These existing mechanisms must be available to the strong control.

Our current-action heuristic is an adaptation in this family, not an original
claim about minimax regret or elicitation. The construction being developed
joins an actual observation source, persistent native solving, separately paid
independent lower proofs and reusable uniform output certificates. An empirical
advantage for that joined service has not been established.

## Why a greedy theorem is not supplied by monotone evidence

Golovin and Krause (2010), *Adaptive Submodularity: A New Approach to Active
Learning and Stochastic Optimization*.
[Author paper](https://www.cs.cmu.edu/~dgolovin/papers/colt10.pdf), Section 2,
Section 3 Definitions 1–2, Proposition 3 and equation (5), PDF pp. 2–4.
The framework specifies a prior over item outcomes. Its greedy guarantees
require adaptive monotonicity and adaptive diminishing returns under that
prior. Conditional expected gain is therefore a probabilistic object, not a
property supplied by an uncertainty set alone. We import this distinction;
we do not import an approximation guarantee for our certificate objective.

The audit-and-proof construction in [the theory note](acq_theory.md), Section
5, has complementary purchases. That is a constructive reason to retain small
bundles when singleton scores vanish. For example, if the audit outcome y has
positive prior mass above one half, the proof has zero gain before that audit
but positive gain afterwards. Thus the elementary certificate-improvement
objective in that example does not satisfy the required diminishing-return
condition. A different objective or proved special case could still support a
useful guarantee; the branch stays available.

## Shared observations across several output requests

The first runnable [joint service](joint_repair.py) retains one cost cohort
across sixteen different hard-constraint requests. Its initial current-action
policy buys more evidence than the audit-first control on the saved exposure.
A cost observation can improve many later outputs, whereas a source-specific
proof may help only one current hard formula and its future reprises. The next
construction should therefore price the common-source effect, or prove a
small complete purchase bundle. This is a direction from the recorded result,
not a post-hoc declaration that the first policy was optimal.

Actual logical outcomes, native caps and cost observations remain distinct.
An outer regret model can contain different amounts of learned information
without supplying the runtime or outcome law needed by a Bayesian acquisition
rule. Guaranteed progress needs complete outcome/cost contracts; exploratory
purchases can instead remain explicitly heuristic with their receipts retained.
