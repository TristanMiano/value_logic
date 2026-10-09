# P3-07 arithmetic adapter design review

Contributor: ChatGPT (GPT-6 Astra Pro), implementation subagent, 2026-10-09 UTC.
Status: development design and local executable probes only. Agent time is
unmeasured and contributes zero principal Research90 credit. No publication,
gate disposition, successful scientific comparison, or theorem of efficient
mathematical problem solving is asserted here.

## Recommendation and its limits

Use the bounded modular equality `a**n mod m == r`, with the complete public
input supplied to every policy. The scope is `0 <= a <= 8191`, `0 <= n <= 192`,
`2 <= m <= 97`, and `0 <= r < m`. The producer executes ordinary right-to-left
binary modular exponentiation. The checker independently executes left-to-right
binary modular exponentiation. The latter costs at most one more modular
multiplication than the former, rather than imposing a gratuitous linear-in-n
checker bottleneck. Both are trusted local software, not a formal-proof
authentication service.

A useful honest balanced population is a declared finite list of odd primes
`p`, a draw of `p` from a public distribution, and a uniform nonzero residue
`a in 1..p-1`, with `n=(p-1)//2` and `r=1`. For each fixed prime exactly half of
the nonzero residues are quadratic residues, and Euler's criterion supplies
the binary equality. Thus the answer base rate of one half is public. Input
generation needs no private computation of the answer and no hidden
answer-balancing step. An ordinary policy may exploit this structure. This
population does not support a computational-hardness claim: the inputs are
tiny, public, and cheap exact computation or mathematical identities can win.

The paid comparison should evaluate complete policies: forecast, choose an
action or bounded computation, incur any computation timeout, acquire an
answer only after checking, and issue the specified fallback if unavailable.
The controller should keep paired raw false-positive, false-negative, fallback,
and resource features. Repricing the same features under different stakes or
objectives tests decision sensitivity without changing prediction accuracy.

## Existing interfaces inspected

- `v3/checks/03_bounded_logic.py` supplies a capped-transaction finite kernel
  with explicit producer/checker phases, retained partial jobs, query and
  source identities, and objective epochs. It already distinguishes bounded
  transactions from equal CPU instructions. The new adapter retains that
  operational separation and uses actual modular arithmetic.
- `v3/checks/05_dependency_frontend.py` compiles supplied finite Boolean
  programs/tables into the P3-05 comparison machinery. Its program graph and
  table values are supplied model input. It records validation, compilation,
  table-row, and binding work. The portfolio machinery also exposes bounded
  proof construction, verification, and search counters.
- `v3/checks/06_mathematical_forecast_development.py` provides the public
  modular scope, residue-level semantic caching, elementary exact shortcuts,
  and ordinary fast exact baseline. Its producer and checker are executed by
  an external schedule before eventual admission. The new P3-07 adapter makes
  the computation/checking/acquisition path itself a paid policy operation.

These prior files and their stored evidence were not modified.

## Exact API and information boundary

The new module is `v3/checks/07_computation_adapter.py`, version
`p307-modular-computation-adapter-v1`. Load it with `importlib` because its
filename begins with digits.

```python
q = Query("q1", 7, 47, 97, 1)
meter = Meter(2000)
adapter = Adapter(meter, cache_cap=0)  # New instance is a cold episode.

answer = adapter.lookup(q)
if answer is None:
    answer = adapter.shortcut(q)
if answer is None:
    handle = adapter.start(q)
    progress = adapter.advance(handle, MAX_FULL_TRANSACTIONS)
    if progress.checked_ready:
        answer = adapter.acquire(handle)
# When answer is None the complete controller uses its charged fallback.
```

`Query(query_id,a,n,m,r,source_version="modexp-input-v1")` is immutable and
validates exact scalar types and finite limits. `residue_key` includes the
semantics version, source version, `a`, `n`, and `m`. `claim_key` additionally
includes `r`. The display ID does not define a mathematical proposition.

`Meter(limit_total, category_limits=None)` enforces an integer hard cap before
funding an operation. `.pay(category, operation, units=1)` and atomic
`.pay_many(tuple_of_triples)` allow the controller's own real operations to use
the same accounting boundary. `.snapshot()` is harness instrumentation, not a
source of hidden outcome information. Declared categories are:

| Category | Meaning |
| --- | --- |
| `admission` | Bounded query validation and semantic identity input |
| `solve` | Producer operations and attempted elementary shortcuts |
| `check` | Independent checker operations and identity-witness checks |
| `acquisition` | Checked record admission and target interpretation |
| `storage` | Declared record/state word reads, writes, and releases |
| `cache` | Exact lookup and full semantic input comparison |
| `forecast` | Controller-supplied charged prediction work |
| `assessment` | Controller-supplied charged policy assessment work |
| `profile` | Controller-supplied profile acquisition/retention work |
| `dependency_compile` | Not applicable to this adapter; zero |
| `repair_search` | Not applicable to this adapter; zero |

`Adapter.lookup(q)` performs a paid exact semantic scan of at most 32 cached
residues. `Adapter.shortcut(q)` pays for actual tests of the cases `n=0`,
`a mod m=0`, `a mod m=1`, and `a mod m=m-1`; a failed attempt is still charged.
Successful identities are independently checked by their local witness
conditions and then acquired. These same methods must be available to every
decision method.

`start(q,algorithm="binary")` returns an immutable `JobHandle`, and
`advance(handle,transaction_cap)` returns only a `Progress` record: phase,
completed transactions, spent units, and whether the hard budget was
exhausted. Neither object exposes a mathematical answer. An insufficient
allowance preserves the unfinished private job. `acquire(handle)` is valid
only after independent checking; the acquisition and cache publication are a
single paid bundle. A denied bundle does not publish the result or a cache
entry. `cancel(handle)` is a paid release operation.

The underscore-prefixed implementation state is private to the trusted
experiment. It is not a Python sandbox against a malicious controller. A
controller that directly reads `_jobs`, uses the harness's truth scorer, or
calls a separate uncharged `pow` violates the experiment interface. The
development tests use those private paths only for adversarial checks and
independent output verification.

## Costs, hard limits, and uniform full-response bound

The unit model counts the explicit bounded operations in the code. A modular
multiplication, reduction, bit test, shift, or declared Boolean test costs one
abstract unit. Record storage is represented in 64-bit words, with labels
counted by their length where they form semantic input/receipt records and
fixed record slots represented as word references. This is a declared abstract
representation, not Python `sys.getsizeof`, physical RAM traffic, equal CPU
cycles, or wall time. Every modulus is at most 97, so modular products are
below 9409 and require at most 14 bits. The source label is at most 128
characters; semantic input keys require at most 24 represented words.

Failed arithmetic funding may follow a successfully paid public-input
preflight. The guard/bit operations already executed remain charged even
though that computation transaction did not finish. This matters for timeout
and near-budget cases: the complete response must use the observed meter
total, not only the number of successful transactions. The event log is
separate bounded audit instrumentation. Input generation and private test
scoring are also harness operations; if either supplies reusable information
to a policy, the information procurement must be charged by the controller.

For an initially empty cache and no controller/profile work, the public
lookup/shortcut/start/complete/check/acquire path has this loose uniform bound:

| Component | Safe maximum charged units |
| --- | ---: |
| Cold lookup including input admission | 33 |
| Failed shortcut including input admission | 38 |
| Binary job creation including input admission | 66 |
| Eight producer iterations and phase completion | 90 |
| Independent checker initialization | 7 |
| Eight checker iterations and final comparison | 83 |
| Checked acquisition, output, and cache retention | 112 |
| **Total bound for full binary path** | **529** |

The producer performs at most eight bit iterations, and the checker performs
at most eight. Their phase completion, checker setup, and final comparison
add three transactions, so `MAX_FULL_TRANSACTIONS=19` suffices. The table
intentionally rounds several sub-bounds upward. Successful-shortcut paths are
smaller than the same bound. The exported
`MAX_COLD_COMPLETION_UNITS=1024` safely covers either cold path. A bounded warm
cache contributes at most `32*24=768` key-comparison units, and the possible
single FIFO release is at most one additional unit, so
`MAX_WARM_COMPLETION_UNITS=2048` safely covers the public path with a full
warm cache. These bounds exclude forecast, policy assessment, profile
procurement, extra repeated calls, cancellation, and the final fallback;
those operations must be added when bounding a complete decision policy.

The module caps active jobs at four, cached residues at 32, one `advance` call
at 256 transactions, total response units at 10,000,000, and audit events at
100,000. A low `limit_total` or category cap can prevent even admission or
acquisition. Controllers should reserve or precommit the work needed for
their complete response, including the specified fallback.

## Self-performance acquisition and fair comparison

The first experiment can use independent draws with a fresh adapter and empty
cache for every episode. A performance profile is then a bounded collection
of observed paired raw feature outcomes from prior paid complete-policy
trials, bound to the task generator, policy versions, resource model, and cold
state. It is not a supplied future outcome law. If the experiment later uses
warm caches, it must identify that cache state or justify transport to the new
state; a cold profile is not automatically a valid warm-state predictor.

Known public analytic facts, including the quadratic-residue base rate and
deterministic bit-length structure of binary exponentiation, are available to
the ordinary comparator. Full exact computation uses the same producer,
checker, shortcuts, and cache as the candidate. The profile's procurement and
assessment costs can make the candidate lose. Equality with an ordinary
decision rule is also a legitimate result. The experiment should retain
those outcomes rather than treating tiny arithmetic tasks as evidence of a
special prediction advantage.

## Dependency and repair boundary

No synthetic compiler or repair bill was added merely to populate a cost
column. Exact source-version equality changes cache admissibility. New stakes
and a new target `r` can use an unchanged exact residue. This is direct
semantic reuse, not a P3-05 dependency transport proof.

If the principal experiment includes a separate P3-05 compilation/repair
witness, it should execute that actual compiler and actual bounded candidate
search, charging the corresponding validation, compilation, proof search,
checking, and retained-record work. The supplied table/graph model must remain
visible as supplied input. The arithmetic experiment alone reports
`dependency_compile=0` and `repair_search=0`, both not applicable.

## Development verification

`development/adapter_agent/test_adapter.py` checks actual producer and checker
outputs against private Python `pow` on a systematic scope sweep, tests
shortcuts, probes every total budget from 0 through 649, and verifies partial
job behavior. It also rejects an injected producer error, prohibits acquisition
before checking, preserves the cache on acquisition denial, distinguishes a
source-version edit from a target/display-ID edit, and rejects Boolean/float
aliases in exact handle identities. Its `--output` option refuses existing
evidence. These tests validate the adapter boundary and arithmetic; they do
not evaluate policy value or establish a scientific win.
