# Reusing a search partition when the formula changes

Contributor: **ChatGPT (GPT-6 Astra Pro)**. October 12, 2026 UTC.
DEVELOPMENT derivation. This is a prospective generalization of
[weight repricing](maxsat_reprice_findings.md); no changed-hard-clause
implementation or performance experiment is claimed.

## The reusable object can be weaker than the old proof statement

The current repricer fixes hard clauses and soft-clause meanings. A different
bridge is possible if a retained binary search tree is separately checked
as a partition of the assignment universe. Each internal node branches on
both values of an unfixed Boolean variable. Its leaves are disjoint partial
assignment cubes whose union is the root domain. That structural fact does
not depend on why the original solver stopped in each cube.

For a new instance on the same variable interpretation, evaluate each cube:

- If a current hard clause is already false throughout it, mark the cube
  infeasible.
- Otherwise sum the current nonnegative weights of soft clauses forced
  false throughout it. Call that number ell_c.

Every currently feasible assignment lies in one leaf and has cost at least
that leaf's ell_c. Hence `min_c ell_c`, omitting currently infeasible leaves,
is a lower bound on the new optimum. Recheck each retained full witness
against the new hard clauses and re-evaluate its objective; the cheapest
surviving witness supplies an upper bound and a feasible action.

An old hard-conflict leaf can become feasible after clause removal. The new
procedure then assigns it its current soft-cost lower bound instead of
silently retaining its old infeasibility. After additions, an old witness
may cease to be feasible and is removed from the feasible action archive.
Neither situation reinterprets a failed witness as a negative answer.
Replacement remains an available action in the repair setting, even when
no retained repair witness survives.

This is standard branch-and-bound abstraction applied to a paid reusable
partition. It preserves a consequence of old search without claiming that
the original refutation still proves a modified formula.

## Root-domain and source checks are essential to this bridge

A tree created under assumptions may cover only their root cube. It can be
used unchanged only if every currently feasible assignment is known to lie
in that covered domain. Otherwise include the uncovered region with a valid
coarse lower bound or obtain additional covering partitions. Dropping old
assumptions does not turn a conditional tree into a global certificate.

Keep the variable map, full branching coverage, current clauses, nonnegative
objective convention and feasible-witness checks bound to explicit versions.
The current stored MaxSAT trees cover the whole fixed Boolean universe; a
more general solver's learned clauses, omitted branches and preprocessing
need their own checked coverage account. This derivation does not grant that
account to an arbitrary solver log.

## Local updates can reuse more than scalar bounds

For a fixed checked partition, a clause can be indexed by the leaves where
its literals are all false. A soft-weight change updates those leaf costs;
a hard-clause change updates their conflict counts. A minimum structure over
currently feasible leaves then maintains the lower bound. Leaves with several
hard conflicts remain infeasible when only one conflict disappears.

Compilation, incidence storage, affected-leaf updates and minimum maintenance
are paid work. A clause may affect many leaves, and the partition can be
exponentially large. No universal compactness or runtime advantage is implied.
When a leaf's lower bound becomes the bottleneck, new search can refine that
cube while retaining other cells, offering a concrete local-repair strategy.

The existing **incremental IHS/IPAMIR** methods are relevant comparisons for
objective changes, clause additions and assumption updates; their conditional
cores already preserve structural consequences across changes
([primary-method bridge](reprice_sources.md)). A simple sound combination is
to take the maximum of separately warranted tree/partition and core bounds.
Whether this extra representation repays its compilation cost belongs to
the next paid-service development, rather than to an unsupported superiority
claim from this derivation alone.
