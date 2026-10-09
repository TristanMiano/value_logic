# P3-B primary-source scope check

Contributor: **ChatGPT (GPT-6 Astra Pro)**. October 9, 2026 UTC.
This is a narrow source-comparison check for the technical gate and optional
recurrence advice. It does not repeat the completed literature work, import a
new theorem into the current implementation, or start a recurrence.

## Logical Induction

Garrabrant, Benson-Tilsen, Critch, Soares and Taylor,
[Logical Induction](https://intelligence.org/files/LogicalInduction.pdf),
Definition 3.0.1, Theorem 3.6.1, Theorem 4.3.6, and section 5.5 were checked
against the primary paper. Its criterion concerns exploitation by every
efficiently computable trader relative to a deductive process. Recurring
unbiasedness is a limit-point result under its sequence and weighting
hypotheses. Proposition 5.5.1 rules out a computable general convergence-rate
function of the stated kind over a theory representing computable functions.
The runtime discussion does not promise an efficient implementation.

**Gate consequence, by comparison:** P3-03's bounded fixed-query resolution
and P3-06's finite-feature/finite-expert scalar guarantees answer selected
operational duties. They do not establish this criterion. No universal
convergence rate, arbitrary mathematical anticipation, or general self-trust
is imported. The existing narrower statements are sufficient for the declared
technical gate; their exact limits must survive into the challenge design.

## Rational metareasoning

Hay, Russell, Tolpin and Shimony,
[Selecting Computations: Theory and Applications](https://people.eecs.berkeley.edu/~russell/papers/uai12-meta.pdf),
Definitions 6 and 8 and Theorems 4, 5, 7 and 9 were checked. Computation is
priced in a metalevel decision process. The myopic policy's decision to
continue implies continuation by the optimal policy; the reverse need not
hold. The stronger stopping implication requires a set closed under
transitions on which the myopic policy stops throughout. The expected
computation-count bound uses the value of perfect information and positive
per-computation cost.

**Gate consequence, by comparison:** P3-07's finite complete-policy selector
and supplied-prior acquisition planner are distinct services with their own
proofs. Neither a positive post-acquisition gain nor a one-step lookahead is
an unrestricted optimal computation policy. Costs already paid at an earlier
root remain relevant to deciding whether to acquire the profile at all.

## Ordinary selective-feedback comparison

Stoltz,
[Information incomplète et regret interne en prédiction de suites individuelles](https://stoltz.perso.math.cnrs.fr/Publications/TheseStoltz.pdf),
chapter 5, sections 2–3, Figure 2 and Theorems 5.1–5.2 were inspected. The
label-efficient exponential-weighting construction uses random revelation
and inverse-probability loss estimates. Its expected-query and
high-probability query/regret statements are distinct. The source itself
notes that the Bernoulli procedure can request more than its nominal query
count. The high-probability bound is not a pathwise hard cap.

**Gate consequence, by comparison:** an optional paid-feedback extension
has an established ordinary comparator. An application must add its actual
acquisition and controller costs and preserve the theorem's feedback
chronology. Capping purchases, allowing their answers to change the current
action, or using the observed subset as the whole evaluation population needs
a corresponding argument. None is supplied merely by citing this source.

## Evidence and attribution

The principal inspected these public primary sources on October 9, 2026 UTC.
Locators identify the mathematical scope; this record does not redistribute
the PDFs. The recurrence review independently records its own source
inspection in [its manifest](reviews/recurrence_agent/sources/manifest.json).
The statements labelled gate consequences are this project's comparison and
inference. The source statements retain their authors' assumptions and do not
become results of Value Logic.
