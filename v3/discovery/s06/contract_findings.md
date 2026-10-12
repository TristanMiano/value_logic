# A paid complete-call option for calibrated repair

Contributor: **ChatGPT (GPT-6 Astra Pro)**, October 12, 2026 UTC.
DEVELOPMENT auxiliary construction for s06. No helper time is credited to the
principal clock. This extends [the acquisition derivation](acq_theory.md) with
a source-bound complete-call option and a sufficient two-outcome purchase rule.
It does not establish acquisition optimality, a native runtime law, a material
economic advantage or readiness for confirmation.

## What this adds

The current native IHS adapter is useful but its caps permit no progress.
Therefore its worst-outcome guaranteed certificate gain can be zero. On the
specific eight-variable source family, the existing branching proof provider
has a simple finite operation bound. Its own `Meter` cap can be set above that
bound before purchase. This provides an additional complete-answer option under
normal uninterrupted execution, with separately paid search, independent
checking, compilation and retention. It does not make a native hint into proof.

The [runnable quotation](contract_quote.py) also provides a sufficient interval
of logical query budgets that will close a requested regret gap in **either**
SAT or independently checked UNSAT outcome. The calculation uses only admitted
cost supports, retained actions/proofs and the public Boolean objective domain.
There is no probability distribution over the next audit or solver outcome.

A new caller should use [the admission guard](contract_guard.py), whose pinned
provider, compiler and quotation hashes reject a later implementation change
before reusing the derived cap. [Its recorded admission](contract_guard_results.json)
performed no additional search and keeps the actual code read/hash fee separate
from each quoted wrapper call. The code binding is not an admission shortcut
for unseen witness or proof bytes: those still undergo the actual checker.

## 1. The finite procedure has a source-bound tariff ceiling

The actual implementation read is
[`budget_provider`, `checked_objective`, `check_negative` and `proof_words`](../s05/maxsat_repair.py),
with [`compile_witness` and `compile_tree`](../s05/maxsat_reprice.py).
The executed result binds their SHA-256 hashes. The provider branches only on an
unassigned variable. For n variables its complete recursion has at most

```text
T = 2^(n+1)-1 nodes,       F = 2^n leaves.
H = sum_hard_clauses (1 + clause_length).
S = sum_soft_clauses (2 + clause_length).
```

For m soft clauses, a conservative bound on the provider's **declared tariff** is

```text
K_provider = T * [2 + H + S + max(2, m+1, n)].
```

The two initial units cover the branch-node and budget-comparison entries.
H bounds all hard-clause header/literal work; S bounds all soft-clause work
including every possible forced-weight addition. The maximum bounds whichever
terminal or split-construction charge occurs at that node. Summing that ceiling
over all possible nodes also safely charges branches that would stop early.

For independent negative checking, the analogous ceiling is

```text
K_negative = T * [1 + max(max_hard(1 + clause_length),
                         sum_soft(3 + clause_length), 0)].
```

Each node costs one entry; a hard leaf inspects one clause, whereas a weighted
leaf can inspect every soft clause plus each index and weight addition. For the
actual compact-tree compiler, `T*(m+2)+F+1` bounds node reads, forced coefficients,
leaf deduplication and retained masks. Raw proof storage is bounded by
`2*(F-1)+F*max(2,m+1)` words under this declared representation. These are loose
ceilings with a short proof, not observed runtimes or predictions of search.

For the sixteen public s05 formulas, there are eight variables, eight unit soft
clauses and either eighteen or twenty-four three-literal hard clauses:

| Declared operation component | 18 hard clauses | 24 hard clauses |
|---|---:|---:|
| Branch provider ceiling | 54,677 | 66,941 |
| Independent negative-check ceiling | 16,863 | 16,863 |
| Compact-tree compilation ceiling | 5,367 | 5,367 |
| Illustrative full wrapper tariff ceiling | 79,964 | 92,276 |

The wrapper additionally checks a supplied feasible incumbent, admits source
words, updates objective words, checks/compiles the returned witness or proof,
retains the receipt and charges its output fields. The provider ceiling stays
below the existing 1,000,000-unit proof cap for this family under repricing,
because its tariff counts weight operations rather than weight magnitudes.
The resulting masks remain meaningful only for the unchanged hard clauses,
soft clauses, variable meanings and source identity.

**Scope of completion and cost:** the ceiling proves that this code's tariff
cap does not interrupt the finite procedure for admitted inputs. It does not
bound CPU time, memory allocator behavior, arbitrary integer bit complexity,
host interruption, file transfer or actual monetary cost. The wrapper records
CPU/wall time separately; its named word/operation tariff is a declared billing
model, not a hardware model. Source hashing, Python bookkeeping and serialization
are not each separately counted by `Meter`; their execution must remain in the
measured-resource component of any fuller deployment bill. The archived result
file itself is an evidence artifact, not a free production storage service.
A host/deadline interruption still produces an unresolved attempt. A prospective
monetary completion guarantee needs an actual fixed fee or further resource quote.

The native adapter can retain its warm state and try first. A deterministic
complete fallback must then be reserved and paid separately, even when native
work produced only an advisory lower hint. Charging the sum of native attempt
and fallback is essential. A native-only spending cap cannot borrow this
separate procedure's completion property.

## 2. A two-outcome query can be priced before buying its answer

Let W be the nonempty warranted common set of nonnegative penalty vectors. For
s06 the target is the fixed cohort sum; divide costs and tolerance by the cohort
size to report means. Let U be the cheapest retained fixed action's uniform cost
cap, including replacement at p. Let ell be a checked uniform scalar lower
bound on the best repair, clipped at p. These can be obtained conservatively as

```text
U   = min(p, min_admitted_witness_u h_W(u)),
ell = min(p, max(0, max_admitted_proof_P min_leaf_v [-h_W(-v)])).
```

A richer existing action/proof certificate may be much tighter; always retain
it and cap the post-purchase bound by the best current B. The scalar envelope
here supplies a sufficient quotation, not a replacement certificate engine.

Choose an integral nonnegative query objective q and define

```text
alpha(W,q) = max_(z in {0,1}^m) [h_W(z) - q dot z],
delta(W,q) = max_(z in {0,1}^m) [q dot z + h_W(-z)].
```

For any feasible violation vector z, these imply
`q dot z-delta <= w dot z <= q dot z+alpha` uniformly over W.
Both maxima can enumerate objective masks using the common support interface.
For eight soft clauses that is 256 masks and 512 support queries; it does not
enumerate feasible source models, reveal cost outcomes or call a solver. Cache
reuse can lower repeated calculation cost, which still belongs in the invoice.

Compared with independent coordinate bounds, this retains source dependencies.
For W equal to the convex hull of `(0,2)` and `(2,0)` and q=`(1,1)`, exact alpha
and delta are both 1; the containing box `[0,2]^2` gives both 2. This is an
arithmetic illustration of a common-source effect, not evidence about the
exposed sixteen-request controller.

An integer bounded query asks for a repair with `q dot z <= b`:

* **Checked SAT** supplies a new feasible z with uniform cost at most
  `b+alpha`. Its scalar regret certificate is at most
  `max(0,min(U,b+alpha)-ell)`.
* **Checked UNSAT** establishes integral objective `q dot z >= b+1` for every
  feasible z. It supplies the uniform lower `b+1-delta`, so the retained action
  has regret at most `max(0,U-min(p,max(ell,b+1-delta)))`.

Consequently, a sufficient query budget for tolerance tau belongs to

```text
ceil(U + delta - tau - 1) <= b <= floor(ell + tau - alpha).
```

Every complete admissible outcome then certifies the requested tolerance.
An empty interval means that this sufficient quotation is inconclusive. It
does not show that a useful query or a good action is absent. Signed retained
proof supports, objective-only knapsack bounds, a different q, an audit or a
new witness can improve it. Impossible answers can be removed from the menu
only using paid or already admitted evidence.

The quotation returns a scalar reduction relative to `U-ell`. For acquisition
from a tighter existing bound B, the usable gain is instead
`max(0,B-max(SAT_quote,UNSAT_quote))`. Retaining old evidence ensures that no
actual post-purchase certificate gets worse. If no-progress timeout belongs
to the provider's contract, include B as a third outcome: the guaranteed gain
returns to zero. Completion and answer quality are separate premises.

## 3. A small paid example separates audit and logical purchases

The example is specified in [the focused check](contract_checks.py): hard
constraint `x1 OR x2`, penalties for true x1 and x2, one unknown fixed cost row
with possible values `(3,3)` or `(4,3)`, p=8 and tau=2. Only the both-true witness
is initially retained. A separately paid and independently checked query at
q=`(3,3)`, budget 2, establishes the reusable lower supports `(1,0)` and `(0,1)`.
That setup receipt costs **146 declared wrapper units**; it is not free prior
logical knowledge.

The initial uniform action certificate is B=4, with U=7, ell=3, alpha=1 and
delta=0. The sufficient interval contains exactly b=4. Its completed SAT and
checked-UNSAT outcome quotes are both at most 2. In contrast, auditing the first
cost gives prospective certificate bounds 3 or 4, so its worst-outcome gain is
zero. These are the complete public audit possibilities; no distribution is
assumed and neither hypothetical value is credited as an actual observation.

The actual logical query costs **117 additional declared wrapper units** and
returns the second-variable-only witness, whose uniform regret certificate is
zero. Both logical calls have raw source-bound responses, independent checks,
invoices and measured timings in [the result](contract_results.json). The
support/quotation/check work adds **929 named operation units** across the
whole small demonstration, including its separate margin illustration. This
is a finite constructive check of the rule and implementation. It is neither
a held-out comparison nor a calibrated claim about expected solver cost.

Executed command:

```sh
python v3/discovery/s06/contract_checks.py v3/discovery/s06/contract_results.json
```

There were two new branching calls, zero native calls and zero external cost
observations. Both complete calls obeyed their source-bound tariff ceilings.
The larger s05 formulas were only read for source-based quotations; their
logical outcomes were not searched again. Raw results record the executed
implementation and check hashes so changes require a new recorded version.

## 4. Price regions keep unknown audit and CPU prices visible

Suppose a complete audit and logical purchase have guaranteed reductions
g_A and g_L, with positive fully quoted prices

```text
C_A = a + sigma*K_A + rho*T_A,
C_L =     sigma*K_L + rho*T_L.
```

Here a is the external audit price, sigma the declared software tariff price,
and rho a CPU price. The resource terms must be genuine prospective quotations
for a guaranteed purchase decision. With g_L>0, the audit has at least as much
local guaranteed reduction per price exactly when

```text
a <= (g_A/g_L)*(sigma*K_L + rho*T_L) - sigma*K_A - rho*T_A.
```

This describes an affordability interval instead of inventing a missing price.
If its right side is negative, no nonnegative audit price wins that local
comparison under the stated quotations. If either purchase has unquoted CPU
cost with rho>0, these expressions alone do not give a finite guaranteed
monetary ratio. Measured CPU can instead yield a **retrospective realized-price
region**, which must not be relabelled a pre-purchase runtime forecast.

For whole executed policies, use the equally direct price half-space
`(n_A-n_L)*a + sigma*(K_A-K_L) + rho*(T_A-T_L) + storage_price*(S_A-S_L) <= 0`.
Cancel admission only when it is actually common under the comparison contract.
This includes each policy's own acquired evidence and unresolved attempts.

Singleton guaranteed scores need not find an affordable completing policy.
The complementary audit/proof example in [the theory note](acq_theory.md)
requires looking ahead to a bundle. The complete-call option makes such a
finite robust decision tree concrete on a small domain: each branch carries
its own updated cost row sets, witness/proof bank, solver state and full
remaining quotation. Cap/no-progress branches and planning costs remain in
the tree. This is a conventional robust planning construction; the closest
elicitation comparison remains [the source bridge](acquisition_sources.md).

## Recommended use in the next service increment

### A complete fallback for the current finite source and duty

The six **public** cost vectors in `joint_source.json` have distinct pairs of
coordinates `(0,1)`. For each row, audit coordinate 0 first. Value 1 identifies
that row immediately; otherwise coordinate 1 separates the remaining modes.
Thus eight rows require at most **16 external observations** to determine the
whole cohort-sum penalty vector. This construction uses no hidden realized mode
or mode probability. The [finite cost-tree check](contract_fallback.py) also
minimizes worst row-identification depth over the supported coordinate menu
and confirms depth two. No single coordinate distinguishes all six modes.
Under the product-of-row-sets contract, an unresolved distinct vector in any
row leaves more than one possible sum, so sixteen is also the worst-case
minimum for full exact cohort-vector identification. This is not a lower bound
on the audits needed to deliver a requested action: certificates can close
long before full calibration.

After this full calibration, all weights are known integers. For each request
the clipped optimum `min(C*,p)` lies in a checked integer bracket `[l,u]` with
initial `0<=l<=u<=p=48`. While `u-l>tau=4`, buy a complete bounded query at
`b=floor((l+u)/2)`. Checked SAT permits `u<=b`; checked UNSAT permits `l>=b+1`.
Either outcome reduces the integer gap to at most `floor((u-l)/2)`. Therefore
the worst gaps follow `48 -> 24 -> 12 -> 6 -> 3`: **four complete calls per
request**, hence **64 calls for sixteen requests**, suffice. A checked witness
or replacement is returned from the resulting tolerance gate. Every negative
bound uses the independent checker; no backend optimum enters the proof bank.

[The recorded fallback check](contract_fallback_results.json) evaluates all
49 abstract clipped optimum values in `[0,48]` to check that recurrence. These
are generic integer-bracket cases, not the source's diagnostic optima. It also
checks the public row-identification tree and version admission, with zero
new provider/native calls and zero cost observations. The worst wrapper-tariff
sum is **64 × 92,276 = 5,905,664 units**. The separate code admission is **6,725
units** for the admitted files. External audit prices, audit processing,
controller evaluation and storage beyond this wrapper, and CPU/host costs
remain additional components. No worst-case source-search calls were executed
to produce this bound, and no native execution law is inferred from it.

That 6,725-unit code fee can be common only when a resident consumer actually
retains its admission of unchanged loaded code. The simple `contract_guard`
entry points recheck on every invocation; calling them afresh for all 64 calls
would add **430,400** code-admission units, giving **6,336,064** for those wrapper
calls plus repeated code admission. Neither accounting choice is an executed
full fallback controller here. The remaining acquisition/controller components
must still be supplied, so neither sum is a complete economic price.

This is an end-to-end physical-purchase and declared-tariff fallback for the
small admitted source. It gives the targeted service a concrete completion
option and a conservative alternative bundle to price. It establishes neither
relative efficiency nor a finite CPU/deadline guarantee. The worst-case source
search grows exponentially with variables; the persistent native method is
still the relevant scalable comparison and possible first attempt.

### Continue with targeted acquisition

Make this direct finite fallback available to every comparison arm, retaining
the persistent native method for scalable warm solving. Use cached common
supports to quote a small menu of complete logical calls and cost audits. When
singletons cannot certify useful progress, inspect a small shared-audit plus
proof bundle, with explicit symbolic price regions. The larger scientific
question is whether that combined evidence purchase yields a meaningful output
at justified cost beyond the strongest conventional controller. It remains open.
