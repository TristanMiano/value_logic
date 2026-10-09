# P3-07 — an ordinary exact profile from arithmetic classes

Contributor: **ChatGPT (GPT-6 Astra Pro)**. October 9, 2026 UTC.
**DEVELOPMENT companion.** This is a source-specific ordinary control for
[paid reasoning](07_paid_reasoning.md#64-a-stronger-ordinary-comparator-removes-much-of-the-acquisition-cost).
It provides exact population feature means under the stated finite law and
operation tariff. It does not predict each unresolved answer without work,
prove a general complexity bound, or measure physical runtime.

## 1. Population and exact label counts

For each $`p\in\{17,31,47,61,97\}`$, take every nonzero residue
$`a\in\{1,\ldots,p-1\}`$. The query is
$`a^{(p-1)/2}\equiv1\pmod p`$. All 248 queries are equally likely under
the declared population law. Put $`n=(p-1)/2`$.

**Lemma 1.** Exactly $`n`$ nonzero residues satisfy $`a^n=1`$ in the
field with $`p`$ elements; the other $`n`$ satisfy $`a^n=-1`$.

**Proof.** Multiplication by a nonzero $`a`$ permutes the $`p-1`$ nonzero
residues. Equating the products of the original and permuted lists and
cancelling their nonzero product gives $`a^{p-1}=1`$. Consequently
$`(a^n-1)(a^n+1)=0`$. A field has no zero divisors, and $`1\neq-1`$
because $`p`$ is odd, so every nonzero residue belongs to exactly one of
the two root sets. A nonzero degree-$`n`$ polynomial over a field has at
most $`n`$ distinct roots: if $`r`$ is a root, polynomial division factors
out $`x-r`$, and induction supplies the bound. The two degree-$`n`$
polynomials here partition $`2n`$ residues and each has at most $`n`$
roots. Both must therefore have exactly $`n`$. This proof uses only the
stated prime hypothesis; the implementation separately checks the five
small primes by paid trial division.

Base 1 is positive. Base $`p-1=-1`$ is positive exactly when $`n`$ is
even. Removing those bases leaves the following class counts.

| Class | Representative | Size | Positive count | Negative count |
|---|---:|---:|---:|---:|
| One | 1 | 1 | 1 | 0 |
| Minus one | $`p-1`$ | 1 | $`\mathbf1_{n\text{ even}}`$ | $`\mathbf1_{n\text{ odd}}`$ |
| Ordinary | 2 | $`p-3`$ | $`n-1-\mathbf1_{n\text{ even}}`$ | $`n-\mathbf1_{n\text{ odd}}`$ |

The two ordinary-class expressions sum to $`p-3=2n-2`$. In particular,
the negative count is $`n`$ when $`n`$ is even and $`n-1`$ when it is
odd. The class does **not** have a common truth value. No single
representative label is multiplied by its class size.

## 2. The source-specific resource-path lemma

**Lemma 2.** For fixed $`p`$, one class from the table and one policy from
the fixed six-policy catalogue, every query has the same charged resource
vector and the same checked-completion status under adapter v1.1 and
controller v3, a fresh empty cache, no pending jobs and the default 1,024-unit
response cap.

**Proof by inspection of the bounded program.** Query labels are admitted
under a fixed bounded-ASCII validation tariff; the mathematical key's word
length depends on the fixed source/semantics strings and scalar-field count,
not on the printed query name. All admitted numerical operands fit the fixed
word model. The cold cache lookup always misses. The shortcut eagerly pays
and performs its declared tests. Its successful branch is fixed for class
one and class minus one; ordinary residues take its unsuccessful branch.

If that branch opens a computation, the right-to-left producer's transaction
schedule depends only on the fixed exponent and its bits. Modular products
have a fixed charge even when their values differ. The left-to-right checker
likewise follows the same exponent-bit schedule. Their ordinary modular
invariants give the same final residue, so the success comparison passes;
no exceptional arithmetic failure changes this path. The six- and twelve-
transaction cutoffs and the full cutoff are fixed by policy. Thus phase,
cursor, termination and budget paths coincide within the class. Job identity
starts from the same cold state; successful acquisition, cancellation and
terminal output are charged in the same way. Cache capacity is zero, so
there is no history-dependent retention branch. No policy reads bit-width
audit snapshots or a hidden residue during this process.

This establishes equality of **declared units**, not equal CPU time or equal
processor instructions. It would need a new proof for a multiplication tariff
that depends on the operand's detailed bit pattern, a query-dependent cache,
a changed stopping rule or a changed adapter source. Source identities bind
this lemma's current instantiation.

## 3. Constructing the exact feature means

Run each of the six policies on the fifteen representative queries. For each
class-policy pair, multiply the resulting resource vector by the class size.
If its answer is checked, its error and fallback counts are zero. If it is
unresolved, assign false negatives to the class's positive count for guess 0,
false positives to the negative count for guess 1, and fallback count equal
to the class size for a fallback policy. Sum over classes and divide by 248.
Lemmas 1 and 2 prove that these are the exact fourteen-coordinate population
means. The true cost of every catalogue policy under any constant price
vector is their dot product with those means. Exact minimization over this
fixed catalogue therefore has no sampling penalty.

The [v2 implementation](../checks/07_analytic_profile.py) pays for reading and
hashing its four source files, bounded model construction and retention,
prime checks, class arithmetic, all ninety policy executions, final numerical
validation/hashing and every price readout. Its numerical identity covers
source hashes, law, population size, exact means, class counts and feature
sums, and procurement resources. The encoded core is 5,680 bytes, within the
prepaid 65,536-byte envelope. Raw per-run meter snapshots are external audit
instrumentation; selection reads the bounded numerical table.

The source-specific mathematical lemmas are prerequisites. A human supplied
their proofs in this companion; the implementation is not an automatic
finite-field theorem prover. The tariff does not quantify human theorem
search, program design or proof development. That limitation also applies
to the research effort that designed the sampled controller and its bound.

## 4. Saved result and ordinary comparison

The profile is frozen before the program opens the retained exhaustive
population file. That file can falsify the already constructed means; it is
not an input to their construction. The external check reconstructs all
1,488 query-policy resource/completion pairs, all class feature sums and all
population means. This validation is a separate development expense, outside
the reported deployed construction tariff.

The [v2 result](../work_logs/P3_07_2026-10-09_S1/development/analytic_profile_run_v2/result.json)
records 64,581 total construction units and profile identity
`a084e5129427a85fbaedf445205062ebdfb242a7a84b2b4cd9f3fb930ae0fa54`.
At ordinary resource prices, construction costs 64.581 and one assessment
costs 0.740. The following gains deduct both exactly once; horizons describe
future IID requests under the declared law, not observed deployments.

| Task/resource case | Chosen catalogue policy | Exact expected all-in gain, 64 requests | Exact expected all-in gain, 10,000 requests |
|---|---|---:|---:|
| Low task prices | fallback | $`-65321/1000`$ | $`-65321/1000`$ |
| High task prices | full computation | $`35638361/31000`$ | $`5882867549/31000`$ |
| False positives expensive | full computation | $`35638361/31000`$ | $`5882867549/31000`$ |
| False negatives expensive | full computation | $`35638361/31000`$ | $`5882867549/31000`$ |
| Zero task prices | fallback | $`-65321/1000`$ | $`-65321/1000`$ |
| Storage expensive | full computation | $`-23590171/31000`$ | $`3567605633/31000`$ |

The sampled 1,024-row profile needs 1,692,957 units, and exhaustive paid
acquisition needs 359,918 units when the separate 248 private `pow` checks
are excluded. The class construction is cheaper under this tariff and fixes
the asymmetric cases where conservative sampled selection preferred a guess.
All methods have the same public arithmetic structure available. The strong
ordinary comparison therefore weakens any claim that this population shows
a distinctive advantage from costly sampling or cost-oriented notation.

This comparison does not prove that profiling is never useful. Many service
populations lack a tractable algebraic class description, and the relevant
path distribution can depend on data or history. Nor does the result show
that this class construction is the cheapest possible decision procedure:
at high stakes, simply invoking the charged exact solver avoids selection
and profile construction entirely. A paid profile is useful only when its
additional decision service justifies its extra cost for the declared use.

## 5. Verification disposition

The numerical v1 run is preserved. Its identity construction included large
raw diagnostic snapshots while its tariff funded a bounded numerical table.
V2 explicitly separates the core, checks its prepaid byte bound, and adds a
bounded final-cost arithmetic allowance. The v2 rerun is deterministic and
is labelled as a correction, not a fresh statistical audit.

The focused independent reconstruction is recorded in
[reviews/analytic_profile_agent](../work_logs/P3_07_2026-10-09_S1/reviews/analytic_profile_agent).
Its final disposition is integrated in the P3-07 readiness record. These are
same-model, targeted, nonblind development checks. No P3-06 source or evidence
was changed, and no P3-B/P3-08 work or final challenge is claimed.
