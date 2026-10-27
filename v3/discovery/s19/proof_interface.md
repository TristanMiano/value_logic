# Checked, priced progress: what the proof-bank guarantee needs

Codex (GPT-6), October26,2026. DEVELOPMENT. This specifies an interface and
its limits; it is not a claim of a competitive wall-clock theorem prover.

## Include validation in the procedure

A fixed procedure j names an immutable mathematical claim, source/version,
search policy and checker. It may propose invalid witnesses, fail to halt,
or expose intermediate facts. Its completion time R_j is the total priced
work until the first accepted certificate, including generation, parsing
and verification. An invalid proposal does not count as completion. A
procedure whose failure is proved terminal can be deleted from subsequent
clauses, since it cannot be part of a finite-cost offline proof bank.
A fallible proposal model is therefore permitted; soundness comes from the
checker and the checked request-applicability relation, not model accuracy.
Randomness must be fixed per procedure for the pathwise comparison, with
its seed and resulting work equally available to the comparator.

The completion-only lower bound still applies to the restricted black-box
interface; richer structural evidence can help on particular instances and
is not covered by that lower bound. Creating new procedures on demand or
altering an old one's search policy changes the comparison class. It cannot
be called the same fixed bank without specifying the new benchmark.

## Nonuniform known atomic prices

The unit-step credit implementation extends to positive rational prices
q_jr for successive atomic instructions, provided the next price is known
before that instruction is executed. Let A_jr be their cumulative sum.
Virtual credit grows at unit rate for every procedure in the selected
unsatisfied clause. Stop at the first next prefix threshold A_j,r+1, or at
the request cap. Execute all due instructions at simultaneous thresholds.
Actual work paid is the last reached A_jr, hence no greater than credit.
If a checked proof finishes at step r, its credit is exactly R_j=A_jr; it
cannot appear in later selected unsatisfied clauses. The same dual argument
therefore proves B<=(d+1)OPT for this named tariff too. Zero-cost runs need a
separate finite-processing assumption; they cannot conceal infinite work.

## Unknown nonpreemptible bills break the guarantee

Even one procedure is enough. Repeated requests cost1 to fall back on.
Suppose a deterministic method has finite ratio rho and can only run a
single nonpreemptible proof attempt, learning its cost at completion. On
an instance whose attempt costs1, competitiveness for long horizons forces
an attempt after finitely many fallback requests, say t. Before the attempt
the same observations occur if its cost is M. End that second instance at
the request where the attempt is launched. The online bill is at least M,
whereas offline can fall back for at most t+1. Taking M arbitrarily large
contradicts any uniform finite ratio. This is an information/interface
obstruction, not a theorem about actual timed OS preemption.

## Controller work is additional and can be bounded separately

For a finite supplied CNF bank, initialize each request's unsatisfied
clauses and literal incidence lists. A completed type updates its incident
clauses once; a list supplies the next unsatisfied clause. Let L be total
literal occurrences plus clause/request headers, W actual atomic proof
instructions, T requests and d maximum width. Each virtual event either
executes at least one instruction or exhausts a request cap. Thus there are
at most W+T events; explicit credit updates/next-threshold selection use
O(d) arithmetic operations each. Clause initialization and completion
updates use O(L). A direct implementation needs O(L+d(W+T)) arithmetic
operations, plus persistent prover/checker states and the current request.
This is a proposed implementation bound, not a measurement of the existing
small checker, which uses simpler scans.

Exact rational arithmetic is not constant-cost machine arithmetic. Credit
integer parts are bounded by paid work plus the next step price; denominators
can accumulate the input-price denominators. Bit lengths and arithmetic
costs must be charged for an end-to-end bound. Checkpoint/recovery, memory,
applicability checking and procedure construction also remain payable.
A common mandatory input-read tariff can be added to both methods, but it
does not erase extra controller work. Do not translate the proof-work ratio
into CPU, energy or latency savings without the additional measurements.

## Small meaningful integration target

A resumable truth-table refutation procedure for a fixed finite CNF can
produce one violated-clause witness per assignment. A separate checker
replays these witnesses and accepts only after every assignment is covered.
Generation and checking are both stepped and priced. Different clause orders
are fixed alternative procedures; satisfiable inputs never produce an UNSAT
certificate. Checked core inclusion determines reuse under edited request
contexts. Requests requiring two independently warranted conditions give
complementary CNF clauses rather than one flattened search race.

Such an integration could establish that the abstract scheduler runs on
actual checked mathematical work. It would not establish competitiveness
against unrestricted SAT solving, novel proof search, or practical speedups.
Compare identical shared ordinary scheduling, fallback only and explicit
independent searches; retain all acquisition and validation work.

## Stronger source comparison found during s19

The unknown-threshold query interface itself has a direct prior treatment:
see the additional [literature record](literature.md). Any remaining useful
delta must concern the persistent request/fallback/proof contract and its
resource guarantee. The existing developmental integration remains valid,
including its unfavorable aggregate comparison with fallback. This source
comparison lowers novelty confidence; it is not a reason to tune away that
negative result or to present the interface as new.
