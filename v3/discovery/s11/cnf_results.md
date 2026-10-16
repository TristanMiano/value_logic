# Costed conditional repair on six existing CNF sources

Codex (GPT-6), DEVELOPMENT. [Declaration](cnf_select_plan.md),
[exact summary](cnf_results.json), [summary source](cnf_summary.py).
The six sources and their completeness evidence were inherited from s10;
there were zero new physical truth purchases. The selector was declared after
the fixed-coordinate screen failed to expose useful information on most sources.
All objective weights and fees were declared before this refinement's outcomes.

| Source | Source models | Selected variables | Distinct new masks | Full regret enclosure | Querying with static menu | No-query regret | Certified reduction vs static / no-query |
| --- | ---: | --- | ---: | --- | --- | --- | --- |
| uf20-01 | 8 | 10,9 | 2 | [4.0062758215,4.0062932969] | [7.4201388888,7.4201407433] | [8.4776785714,8.4776811600] | at least 46.0078% / 52.7430% |
| uf20-02 | 29 | 15,5 | 1 | [2.0198936170,2.0198936463] | [4.6437499999,4.6437509060] | [4.6874999999,4.6875] | at least 56.5029% / 56.9089% |
| uf20-03 | 1 | 1,2 | 0 | 0 | 0 | 0 | zero-regret tie; percentage undefined |
| uf50-01 | 24 | 10,42 | 0 | 0 | 0 | 0 | zero-regret tie; percentage undefined |
| uf50-02 | 6 | 23,43 | 5 | 0 | 0 | 0 | zero-regret tie; percentage undefined |
| uf50-03 | 1,362 | 33,41 | 1 | [12.9451777103,12.9451918602] | same enclosure and realized policy | [14.0689655172,14.0689811707] | no enabled-menu gain / at least 7.9876% |

Decimal intervals are rounded outward; JSON retains exact fractions. The first
two cases distinguish evidence that enables an edit from evidence used only to
predict cost. On uf50-03 the optimized policy never uses its newly enabled
mask: predictive information alone explains the gain. On uf50-02 five new masks
do not help the declared objective. Menu counts are therefore not usefulness
metrics. Three sources already admit zero regret without buying information.

The objective includes query fees 1/4 and edit fees 1/8, against the SAME full
operational comparator in all arms. It excludes admission, model enumeration,
query selection, menu compilation, optimization, retention and checking prices.
Those exclusions prevent a complete-cost claim. Every reported upper bound
comes from an exactly realized private policy, every lower bound from a bounded
rational dual correction. The maximum enclosure gap is below 0.000017476.
An ordinary optimizer with the same information and menus ties exactly.

The model-splitting selector reads 464, 1,682, 58, 3,552, 888 and 201,576 model
bits, respectively; it is not an economical or optimal selector claim.
Direct incremental SAT calls versus additional core/witness reuse are
7,366/3,940; 7,647/3,643; 4,977/1,251; 62,688/28,073;
71,339/32,064; 39,537/18,674. Both arms already retain the native solver.
These call counts exclude variable solver effort and added cache/checking work;
they are not percentage reductions in complete counted computation.

All cr01 source-menu cases pass. cr02 and cd01 complete cases 0--3. The two
missing cases complete on first amended-runtime attempts in cr03/cd02, after
the explicitly retained failures in [failures.md](failures.md). No source,
assertion, selector, objective or cap changed. Unsuccessful prefixes remain
costs, not retroactive successes. These results are exploratory reuse of
exposed sources, not confirmation or a claim about typical SAT applications.
