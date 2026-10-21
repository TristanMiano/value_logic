# Learning an operational warrant from failed audits

Codex (GPT-6), DEVELOPMENT, October21,2026. Candidate composition of the
ordinary mistake-bound learner for conjunctions and the action-preimage
compiler. This is a distribution-free *finite revision* guarantee, not a
probabilistic reliability claim or a way to act on an unaudited false model.

Fix a finite clause vocabulary C with M members over a fixed world space.
Every action a has an exactly known success preimage G_a that is a
conjunction of clauses in C. At time t the unknown actual world x_t may be
chosen adversarially. Maintain H_t as the conjunction of a subset C_t of C,
initially C. Choose any affordable action satisfying H_t subset G_a, using
the declared compiler/optimizer. If none exists, use a separately specified
fallback or decline the action. Before any irreversible action, audit G_a.

If the audit passes, execution has its checked success guarantee for x_t.
If it fails, obtain a truthful counterexample clause phi in G_a with
phi(x_t)=false, discard phi from C_t when present, and otherwise use the
entailed-clause argument below. A fallback is separately priced; a failed
proposal does not count as a safely completed task.

## Why a failed chosen action forces a model revision

It is insufficient merely to remove phi: H_t may entail phi without storing
phi. Instead, the failed audit must supply enough truthful information to
identify at least one stored clause psi in C_t violated by x_t. Such a clause
exists because H_t subset G_a and x_t notin G_a. A complete x_t suffices but
may be expensive. For an explicit empirical-vocabulary learner that only
chooses actions whose defining clauses are themselves in C_t, phi is stored,
so its failure certificate suffices. This stronger syntactic choice has the
same available action menu as semantic entailment only when C_t is closed
under consequences within C; checking that closure can have a price.

For the semantic choice, an audit of H_t itself can return a violated stored
clause. Paying for that stronger audit is a different service from auditing
only G_a. Under either explicitly adequate feedback interface, delete one
or more false stored clauses. No clause is reintroduced. Hence there are at
most M failed certified proposals that trigger revision over an arbitrary
sequence of worlds. This counts failures, not audit fees, lost utility or
the number of declines, and does not imply convergence to a useful policy.

## Comparative limitation

Starting with all clauses can make H_t inconsistent, in which case semantic
entailment permits every action until the paid audit intervenes. Successful
audits reveal little about unused clauses. An adversary can repeatedly force
expensive successful audits even after the last model revision. A universal
safe fallback may itself dominate all the proposed actions once those fees
are charged. Thus the bounded-revision statement is established learning
machinery, not by itself a material improvement.

The useful prospective question is whether a naturally bounded clause
vocabulary and cheap reusable failure witnesses can support better task
economics. The statistical coverage construction in learn_permissions.md
and this adversarial revision construction make different promises; neither
silently supplies the other's assumptions.

Primary comparison: Saha's2019 dissertation, [Learning Frameworks for
Program Synthesis](https://samsaha.com/files/learning-frameworks.pdf),
§4.1 and§5.3.2.2, already develops property-directed conjunctive learning
and predicate elimination with bounded rounds. This basic revision proposal
therefore receives no novelty credit. Its§3.2 also treats informative
failure of an incomplete verification engine; a timeout alone does not
satisfy that feedback interface.

One cheap repair to the feedback gap is to remove a nonempty collection of
stored clauses until H_t becomes compatible with the truthful partial
counterexample. This preserves the finite deletion bound without pretending
that each removed clause was individually falsified. It may discard true,
useful constraints. For an implication-only H_t and a failed implication
whose endpoint receipt fixes i1,j0, minimum-weight edge deletion is a directed
i-j cut. General clause deletion does not inherit that tractability. This
is standard minimum correction/graph-cut machinery, not selected for a new
probe without an operational advantage over those existing methods.
