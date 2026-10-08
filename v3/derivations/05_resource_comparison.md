# P3-05 — What reuse saves, and what an ordinary method may retain

Contributor: **ChatGPT (GPT-6 Astra Pro)**, October 8, 2026 UTC.
Status: S3 DEVELOPMENT comparison executed; no confirmatory performance claim.

## 1. Fixed service and controls

The consumer asks for a uniform upper bound on its independently fixed loss
difference over the **entire current incumbent rank sublevel**. This matches the
portfolio's actual guarantee. Computing a tighter bound on just the optimal
repairs is a different service; it is not silently used to make a method look
better. All methods receive the same finite frame, incumbent and explicit old
frame. No future edit outcomes or hidden truth labels are supplied.

Compare four concrete routines:

- **P-REUSE:** construct/admit an old band once, then generate and independently
  receive portfolio proofs for the announced edit sequence. Count construction,
  admission, each edit's generation/receiving work, and stored proof bytes.
- **O-FRESH-CERT:** the same current conditional-proof producer and receiver,
  with no old certificate choices. This is a controlled ablation, not the
  strongest ordinary competitor.
- **O-ADD-COLD:** an exact rational algebraic decision-diagram manager rebuilt
  per current request. It shares subexpressions and operations within each
  request, including Boolean relationships that interval evaluation misses.
- **O-ADD-WARM:** the same manager retains its correctly constructed diagrams,
  expression cache and operation cache after processing the old frame. It
  recomputes the new source/rank query, reusing only unconditional expression
  denotations. Current feasibility and request identities are rechecked.

The ordinary comparator may also use P-REUSE itself; no numerical difference is
claimed under that identity construction. The ADD method is a compact new
implementation of established algorithms, not production CUDD. It computes
an exact answer within a trusted process; its exported nodes are audit data,
not a standalone externally authenticated proof. The certificate methods
produce recheckable witnesses in their smaller trust interface. This difference
must be considered before treating raw runtimes as directly interchangeable.

## 2. Why the ordinary algorithm is exact

The manager represents a rational-valued function of Boolean inputs by a
fixed-order directed acyclic graph. Equal-child nodes are removed and identical
nodes shared. Apply splits on the earliest variable in either operand and
memoizes each operator/node pair. By induction on remaining variables, it
computes the exact pointwise operator; rational terminal operations are exact.
Compiling the finite expression grammar therefore preserves its denotation.
These are reconstructed ordinary decision-diagram arguments, with primary
antecedents in [T05-S9](../literature/05_portfolio_sources.md).

The current guard is the conjunction of the hard constraints and the rank
inequality at the supplied incumbent cutoff. A recursion on the guard/value
node pair explores both assignments at each relevant variable, skips only
false-guard branches, and combines minima/maxima from all nonempty branches.
Induction proves the extrema are attained and exact. It retains witnesses for
both extrema; a checked feasible incumbent prevents a vacuous result.

The ADD order is fixed and the input/resource caps are explicit. Diagrams and
intermediates can still grow exponentially. A short final answer does not imply
cheap construction. The cache stores functions of named coordinate positions
under the unchanged arithmetic/Boolean semantics, not claims that a discarded
premise remains true. A changed loss expression or hard constraint is compiled
and the current query rechecked. Different physical meaning for a supplied
coordinate remains a model-adequacy question outside this exact algebra.

## 3. Measurements and prospective finite cases

Record raw, heterogeneous operation counts; rational component sizes; source
and proof sizes; cache/node counts; and elapsed nanoseconds for each phase.
Do not add a graph lookup, arbitrary-precision arithmetic step, byte comparison
and tree visit as if they had one physically established price. Times are local
development observations, not a statistical population claim. All failed or
unproved cases remain in the output.

Fixed families are: a constant-loss overhead control; two differently associated
parity expressions with the same denotation; tied-source selection changes;
withdrawal requiring a larger loss allowance; and the compiled live/copy/
original-predictor comparison. The parity case deliberately permits ordinary
canonical sharing; any advantage over fresh tree proof search must also be
compared with that stronger route. Construction of old certificates/diagrams
is charged separately and included when computing total repeated-use cost.

An unchanged certified request can of course be cached by any method. This
comparison uses genuinely versioned constraints/ranks and source records.
Even an observed advantage for one declared routine does not establish
superiority to every ordinary implementation, a new logical-induction property,
or an optimal paid reasoning policy. Its purpose is to identify the resource
conditions under which this finite reuse interface is useful or merely overhead.


## 4. Observed result, including the unfavorable comparison

The [first fixed comparison](../work_logs/P3_05_2026-10-08_S3/development/resource_1/summary.json)
passed 14,628 assertions in nine suites. Its separate scalar reference covers
1,536 Boolean function/order pairs and 255 nonempty source/rank combinations.
All 32 specified receiving edits were completed. Every method agreed on the
receiving service, with exact diagram ranges no larger than the requested
certified bound.

The following are total local milliseconds for each full declared family.
Reuse includes construction and admission of its old certificate. Warm ADD
includes its initial old-frame query. Fresh/cold methods have no retained old
preparation to amortize. All raw phase times and counters are saved; rounding
here is only presentation.

| Family | Edits | Reuse | Fresh certificate | Cold ADD | Warm ADD |
|---|---:|---:|---:|---:|---:|
| Constant loss | 8 | 4.635 | 3.590 | 3.292 | 1.965 |
| Parity, 3 bits | 6 | 10.041 | 49.584 | 5.546 | 3.015 |
| Parity, 5 bits | 6 | 21.453 | 159.187 | 10.116 | 4.521 |
| Parity, 7 bits | 6 | 69.393 | 722.432 | 15.173 | 8.105 |
| Optimizer turnover | 2 | 4.523 | 4.030 | 1.794 | 1.576 |
| Withdrawal penalty | 4 | 3.894 | 1.644 | 0.853 | 1.399 |

On seven-bit parity, reuse constructs and verifies six single-node covers,
where the fresh certificate route constructs and verifies 888 cover nodes
across its six requests. This is a concrete saving **inside the certificate
workflow**, not an advantage over canonical Boolean reasoning. Its receiver
also compares more record characters: 10,458 versus 7,272, before charging the
old certificate. Warm ADD ends with 82 diagram nodes, 205 cached Apply entries
and 36 expression-cache entries; their memory is not free. Its node JSON alone
is 1,455 bytes, which excludes dictionaries, cached keys, Python object overhead
and other retained data.

The warm ordinary route is faster than reuse on every stated family in this
one local execution. On the withdrawal control, warm initialization costs more
than restarting the small ordinary solve; retention is not always worthwhile.
The data therefore do **not** establish a general resource advantage for the
proposed receiver, or even a universal advantage for caching. They identify
where supplied proof witnesses reduce repeated proof search and where that
saving is dominated by an ordinary symbolic representation. The distinct
portable-witness/trusted-solver services still need an application-specific
choice; this experiment alone does not price that difference.

An apparent tenfold improvement over fresh seven-bit proof construction would
thus be a misleading headline without the roughly eightfold faster warm ADD
comparison. The ordinary method is not required to repeat exponential truth
enumeration or discard its cache. These are development fixtures selected for
understanding the mechanisms, not a sample estimating real-world speedups.

## Observed amortization and the meaning of the ablation

A [prefix analysis](../work_logs/P3_05_2026-10-08_S3/reviews/resource_prefix_analysis.json)
retains all bootstrap expense and the declared order of edits. Reuse was below
fresh portfolio-certificate construction from the first observed edit in each
of the three parity families. It did not become cheaper than that ablation in
the eight constant-loss edits, two turnover edits, or four withdrawal edits.
These are actual observed prefixes, not an extrapolated expected break-even
horizon. None justifies assuming future requests have the same cost distribution.

The fresh-certificate routine is the current portfolio producer with an empty
old-proof library. The old bootstrap instead uses the inherited rank-band
builder. Consequently, the comparison isolates these *implemented routes*; it
is not an optimal fresh-proof-search lower bound or a universal estimate of the
value of caching. A better fresh builder, algebraic preprocessing, or compilation
of ordinary decision-diagram reasoning into certificates may change the result.
The warm ADD control is allowed to retain and reuse its own successful
computations, which is exactly why it is a more informative ordinary comparator
than a repeatedly restarted exhaustive enumerator. Its favorable result is
retained even though it weakens the performance interpretation of the proposed
proof-reuse workflow.
