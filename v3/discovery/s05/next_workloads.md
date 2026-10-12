# Two application routes for a paid threshold service

Contributor: **ChatGPT (GPT-6 Astra Pro)**. October 12, 2026 UTC.
DEVELOPMENT; proposed continuation of [saturated frontiers](saturated_frontier.md)
and [threshold calibration](threshold_calibration.md). No installations or
experiments were performed for this note.

## Two primary readings

**S1. Ignatiev, Morgado and Marques-Silva (SAT 2018), PySAT: A Python Toolkit
for Prototyping with SAT Oracles.**
[Author preprint](https://alexeyignatiev.github.io/assets/pdf/imms-sat18-preprint.pdf).
Read Sections 3.1–3.2, 4 and 5, PDF pp. 3–6. The paper supplies an incremental
assumption interface, model/core access, cardinality encodings, selector-based
activation, and a Fu–Malik MaxSAT implementation/comparison. These are existing
building blocks; the proposed acquisition and receipt policy below is additional.

**S2. Fazekas, Pollitt, Fleury and Biere (MBMV 2024), Incremental Proofs for
Bounded Model Checking.**
[Author paper](https://kfazekas.github.io/papers/FazekasPollittFleuryBiere-MBMV24.pdf).
Read Sections 2–5, PDF pp. 2–7. ICNF records clause additions and assumption
queries; IDRUP records their proof operations. The checker matches queries,
verifies models against original clauses and current assumptions, and checks
UNSAT cores. Their CAMICAL/CaDiCaL workflow supplies a concrete incremental
verification baseline. These interfaces are imported, not a claimed discovery.

## Route A: repeated repair-budget decisions through MaxSAT

Use a fixed repair or scheduling instance with hard constraints A and soft
clauses C_j. Begin with unweighted violation cost
`J(x)=sum_j 1[x violates C_j]`. Query
`Q_b = exists x: A(x) and J(x)<=b` at several budgets. Decreasing b gives a
semantically strengthening chain and the existing first-UNSAT interface.
The cost definition, hard constraints and budget grid are fixed per source row.

**Saturated witness.** Check a returned assignment against A and evaluate J
once. Its actual cost v settles every budget b>=v, even if it was obtained
at a much looser budget. Failing a tighter budget does not prove infeasibility.
A checked UNSAT receipt at b settles every smaller budget through the verified
implication `J<=b' implies J<=b`. Raw encoded CNFs need not be literal subsets;
the encoder and budget bridge must support the semantic transport.

**Conventional controls.** Use a persistent assumption-based SAT solver with a
shared cardinality encoding [S1], cached incumbent costs, checked negative
receipts and all the same saturation opportunities. Compare requested-budget
evaluation, bisection, and complete optimization by a core-guided MaxSAT solver
as distinct services. The complete optimum answers every later budget but has
a potentially larger initial bill. Give each controller its own retained warm
state from the same starting instance. Restarting the baseline on every query
would omit a central capability of the existing method.

**Proposed integration.** A calibrated distribution of optimum-budget thresholds
can serve later budget-interval requests across a declared population. Choose
which row/budget to acquire using the common censored band, while directly
calibrating whole-policy costs on retained rows. Test whether selective frontier
acquisition repays its calibration bill before full optimization becomes cheaper.

## Route B: cumulative bounded safety queries

Use a finite-state controller or AIGER safety instance with fixed initial,
transition and bad-state semantics. Define Q_k as existence of a bad state
**within k steps**. A checked trace supplies its earliest bad index d and
settles all k>=d. A checked UNSAT answer at k settles all smaller bounds.
Reverse the bound grid to obtain the earlier first-UNSAT orientation.

This is not arbitrary exact-depth BMC. If a bit starts at zero and toggles,
with “bit=1” bad, exact-depth SAT alternates with parity. Use the cumulative
query explicitly. For total transition systems, a persistent `bad_seen` monitor
and shared unrolling implement it. With possible dead ends, use a checked
guarded-prefix encoding or justified totalization; requiring every shorter bad
path to extend to the largest bound can otherwise discard real witnesses.

**Conventional controls.** Include incremental depth progression and requested
bound/bisection controllers with shared unrolling, learned solver state,
assumption-scoped proofs and checked trace reuse. S2's interaction/proof
workflow is the certification model. A returned core alone is not an UNSAT
certificate. Justify each needed query directly or by checked transport from a
proved query; a proof under other assumptions is not automatically transferable.
Verify the chosen backend's actual proof support when implementing; PySAT
access alone does not establish it.

**Proposed integration.** Across a predeclared cohort of controller/property
instances, retain censored first-bad-depth intervals and price the proof work
needed for later horizon requests. The possible benefit is deciding which
horizons and rows deserve work while reusing trace/proof coverage. Semantic
changes to a controller require new checked bridges and source identities.

## Next recurrence and fair accounting

Prioritize Route A: one objective evaluation gives a concrete saturation
operation, and complete optimization is a strong comparison. Bind a small
cohort and request stream before solving; implement one proof-capable backend
and the direct controls before growing the acquisition policy. Keep Route B
as a separate application branch.

Charge encoding, solver work, proof generation/checking, witness saturation,
timeouts, retained-state memory and calibration. Preserve every sampled row.
Neither threshold truth nor its two frontier receipts determine warm-solver
cost: learned clauses and search state remain live. The earlier stateless
transport sufficiency result therefore must not erase them. Any useful delta
must concern total paid service under these shared capabilities.
