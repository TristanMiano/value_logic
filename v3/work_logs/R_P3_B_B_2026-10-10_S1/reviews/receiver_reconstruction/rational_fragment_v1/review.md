# A valid inherited input outside the new ADD evidence fragment

Contributor/model: **ChatGPT (GPT-6 Astra Pro)**, October 10, 2026 UTC.
Same-model independent DEVELOPMENT scope review; zero principal-clock credit.

## Finding

**The new ADD evidence bridge has a concrete proper-domain restriction.** One
valid inherited one-bit request computes a reduced constant with a 7,914-bit
denominator. The old ordinary ADD accepts and evaluates it within its
16,384-bit computed-terminal cap. The new producer rejects it under the
4,096-bit evidence cap, and the unchanged independent receiver rejects the
corresponding attempted oversized wire. The requested bound is nevertheless
true on the entire current sublevel, including both tied minimizers.

The [plan](plan.md), [complete fixture](fixture.json), [diagnostic budget](budget.json)
and [source manifest](source_manifest.json) were saved before the single worker
execution. [Five focused groups passed](run/results.json); all ten captured
files remained unchanged. There was one old ADD query, one new export attempt
and one receiving attempt. No common-service tariff, certificate-delivery
episode or policy run occurred. This is a scope witness, not an experimental
winner or a comparison of fully paid terminal costs.

## Exact mathematical construction

Let $`p_1,\ldots,p_{64}`$ be the first sixty-four distinct primes, ending at
311. Set $`q_i=p_i^{k_i}`$, where $`k_i`$ is the largest positive exponent with
$`q_i\le 2^{127}`$. The fixed input has one Boolean bit, no hard or soft rows,
bound zero, supplied witness `(0,)`, and receiving difference

```math
D=-\sum_{i=1}^{64}\frac{1}{q_i}.
```

Each negative summand is an inherited literal. A balanced binary addition
tree has exactly 64 literals and 63 additions: 127 expression nodes, depth
six from a depth-zero root, and seven levels. Every literal has at most 128
bits per rational component. The exact current Frame record is 4,227 ASCII
bytes. The inherited grammar accepts the request, and the no-soft-row case
has one rank tier with rank zero. Both Boolean points are feasible tied
minimizers and belong to the supplied incumbent sublevel. No source or tie
is discarded to make the bound true. [Input validation and recorded counts](run/results.json)

Define the positive integers

```math
Q=\prod_{i=1}^{64}q_i,
\qquad
N=\sum_{i=1}^{64}\frac{Q}{q_i}.
```

For each selected prime $`p_i`$, every term of $`N`$ except $`Q/q_i`$ contains
the factor $`q_i`$. The remaining term is a product of powers of other primes.
Therefore

```math
N\equiv Q/q_i\not\equiv0\pmod{p_i}.
```

Those are all the prime factors of $`Q`$, so $`\gcd(N,Q)=1`$. The reduced
receiving difference is exactly $`-N/Q`$ and its denominator is the complete
product, without cancellation. The independent check uses integer products,
exact divisions, a numerator sum, residues and gcd; it imports no ADD,
interval or portfolio calculator for this computation. The complete exact
integers and residues are saved in [independent_exact_bound.json](run/independent_exact_bound.json).

The separation was established before execution. Maximality of each prime
power and the bound on its base give

```math
2^{118}<2^{127}/311<q_i\le2^{127},
\qquad
2^{7552}<Q\le2^{8128}.
```

Also $`N/Q<64/2^{118}<1`$, so $`0<N<Q`$: the numerator fits whenever this
denominator fits. Every proper balanced subtree has at most thirty-two
leaves, so its denominator has at most 4,065 bits under the conservative
pre-run bound. Its negative numerator is smaller in magnitude. The root
alone necessarily crosses the new 4,096-bit cap while remaining within the
old 16,384-bit cap. The run supplied the following exact component sizes.

| Quantity | Exact bits |
| --- | ---: |
| Largest input literal component | 128 |
| Largest proper-subtree denominator | 3,981 |
| Absolute final reduced numerator | 7,797 |
| Final reduced denominator | 7,914 |

Every summand is strictly negative, so the constant satisfies the bound zero
at both Boolean points independently of its large reduced denominator. The
fixed witness is feasible and the complete rank-zero sublevel is nonempty.

## Source-bound implementation outcomes

The [old ordinary ADD](source/v3/checks/05_ordinary_add.py) validates each input
expression through the inherited grammar, but permits computed terminals up
to 16,384 bits per component. Its single `Manager.query` succeeded with status
`EXACT_CURRENT_SUBLEVEL_RANGE`. Both endpoints equal the independently
calculated $`-N/Q`$; the maximum recorded rational component is exactly 7,914
bits. The query constructed 129 terminal nodes, including zero and one,
65 Apply cache entries and 127 expression bindings. Its private audit export
does not by itself constitute a checked imported certificate.
[Successful old report](run/old_add_report.json)

The [new recording producer](source/v3/checks/05_add_evidence.py) checks its
4,096-bit terminal cap before calling the old manager's terminal insertion.
A normal `RecordingManager` and `export_dag` attempt reached the final
7,914-bit result and raised `EvidenceLimit: Evidence rational component cap.`
All admitted proper-subtree terminals fit within 3,981 bits. The saved partial
state has 128 nodes, 64 recorded Apply facts and 126 expression bindings. The
final expression and final Apply result were not inserted. **No wire was
emitted by the new producer.** The rejected work counters and complete partial
state remain preserved. [Rejection](run/new_producer_rejection.json),
[partial state](run/new_producer_partial_state.json)

To examine the receiver separately, the diagnostic completed the bad-set
predicate using the old manager's actual operations and serialized its actual
node, Apply and expression tables into the declared wire shape. This was a
labelled attempted out-of-fragment packet, not output attributed to the new
producer. It contains the same full Frame, source record, witness, bound,
order and current roots. Its total size is 66,203 bytes, well below the
32-MiB wire-size cap. [Attempted packet](run/attempted_out_of_fragment_packet.json)

The [unchanged independent receiver](source/v3/checks/05_add_evidence_check.py)
rejected that packet with `Rejected: JSON integer syntax or digit cap.` Its
1,234-digit integer parser bound is encountered before its later 4,096-bit
terminal validation on this large integer. It admitted zero nodes, zero Apply
facts and zero expression bindings, and returned no current receipt. No cap,
parser, worker source or private receiver state was changed to obtain either
an acceptance or this rejection. [Receiver rejection and state](run/receiver_rejection.json)

The ordinary query's additional two bad-set completion operations are recorded
separately in that receiver artifact. Raw work counters and serialized sizes
describe this diagnostic; they do not price setup, transmission, checking,
storage and terminal delivery under the common benchmark tariff.

## Precise consequence for the bridge claim

This is more than a difference between two displayed constants. The current
wire requires an independently checked exact expression binding for the
specified receiving difference, with a corresponding ADD root. A decision
diagram representing this constant on all Boolean points must contain its
exact terminal value: each path ends in that same value. Here the reduced
denominator alone has 7,914 bits, which cannot occur in an admitted terminal
under the unchanged 4,096-bit rule. Altering the source expression or replacing
the receiving obligation with a different current record would change the
independently supplied input. This exact root format therefore cannot provide
a total bridge over all valid inherited inputs accepted by the old ADD.

The result does **not** show that the receiving inequality requires a large
certificate in every proof system. Its sign follows directly from the negative
summands. A proof language with an appropriate compositional inequality rule
can express that argument without exporting the exact reduced sum as a
terminal. Nor does this run show an end-to-end economic advantage of the old
ADD or of a native method. It establishes a concrete boundary of this recorded
ADD/exact-root evidence format and its producer.

The valid narrower description is that the implemented bridge works inside
its declared evidence fragment, including the 4,096-bit computed-terminal
condition and the other fixed source, grammar, table, receipt and wire limits.
The original inherited 128-bit **input** cap does not imply that condition.
The published finite primary fixtures remain separate evidence; this scope
witness does not rewrite their sources, outputs, prices or results.

## Reproduction and immutable evidence

The diagnostic ceiling was thirty process-CPU seconds with a thirty-one-second
hard limit; it was not a priced bill or a principal research allocation. The
single execution completed all five expected groups. No unexpected failure
or source change occurred. All expected rejections are retained.

Run from the repository root with a fresh output directory:

```bash
python v3/work_logs/R_P3_B_B_2026-10-10_S1/reviews/receiver_reconstruction/rational_fragment_v1/source/v3/work_logs/R_P3_B_B_2026-10-10_S1/reviews/receiver_reconstruction/rational_fragment_v1/scope_probe_v1.py \
  --source-root v3/work_logs/R_P3_B_B_2026-10-10_S1/reviews/receiver_reconstruction/rational_fragment_v1/source \
  --manifest v3/work_logs/R_P3_B_B_2026-10-10_S1/reviews/receiver_reconstruction/rational_fragment_v1/source_manifest.json \
  --out /tmp/rp3bb_rational_fragment_reproduction
```

| Source or artifact | SHA-256 |
| --- | --- |
| Old ordinary ADD | `9263992673a815b15b489272aa827ea27066a0af264a85bbf905875f632abef7` |
| New producer | `1e40f1bf7a3cb2dc9cfe46beff9a3548392e99e7ff0fa81a6c79c2f53508bbdc` |
| Independent receiver | `1f396bbb625614c87d48fa5fece438851999a7afeb58d5af6933812b4038c2bf` |
| Pre-run fixture | `7708e40baa12f8c31a88f8babab166196b2d52d8ce1f79deb00a974047884250` |
| Pre-run diagnostic budget | `15cad06a8b8917ecf46fd15a973c2477e96fd7cf6eae3dab6196232adfeafb23` |
| Diagnostic source | `0915bd37591b6b9e9e14ea43a230e2e482b3e76d82eb133d05ee562363791421` |
| Captured source manifest | `450b97005d57767b277f80b17f40ca361a437b1518a77c4a29a6eb983f4100e0` |
| Complete results | `592f70a5de7c85dec0256411eacc08eb660c1f02298360b6ca5b7aa5faa0a60e` |

This review ends after the one declared diagnostic and focused Markdown source
verification. It makes no global style or live-rendering claim and adds no
scientific timing credit.
