# Two different limitations of the bounded rational checker

Codex (GPT-6), October24,2026 UTC. DEVELOPMENT. This review found a
reproducible availability defect, repaired in a new version, and a separate
mathematical incompleteness. The historical [s16 checker](../s16/block_check.py)
and its executed evidence remain unchanged.

## Valid premises can require an out-of-format witness

Let the bit cap be B>=5, v=2^(B-2), and use scalar inputs

    C=(v+1)/(2v+1), E=(v-1)/v, V=1, threshold=1.

Every numerator/denominator fits B bits;0<C<1 and E>0. Direct algebra gives

    U_t(C)<1 iff t>EC/[1-(1+E)C]=v^2-1.             (F1)

Here1-(1+E)C=1/[v(2v+1)]>0. Every admitted positive rational t has
numerator at most2^B-1 and denominator at least1, so t<=2^B-1<v^2-1.
Thus no permitted upper parameter certifies below1. Nevertheless t=v^2
is a mathematical strict certificate and satisfies the cap (E<1,t>=64).
The sharp endpoint is below1. No sound lower certificate can certify above1,
so every permitted certificate is unresolved.

At B=4096 the premises also fit the raw-digit and byte limits. F1's
threshold has8188 bits; the displayed witness has8189. The decision
threshold itself is the one-digit rational1. Fixed-format completeness
therefore fails even with all premises inside the input limits.

## Output serialization defect and repair

[format_probe.py](format_probe.py) uses those premises, the largest allowed
upper parameter, and two lower parameters. Lower t=2 returns unresolved.
Lower t=2^B-2 is also admissible, but its exact output has a decimal component
longer than Python's default4300-digit conversion limit. The original
`verify` finishes its arithmetic and raises ValueError at `str(lower)`.
The [observed record](format_result.json) preserves the message and original
checker hash. No false approval was observed.

[block_check_v2.py](block_check_v2.py) changes only result serialization,
emitting integers in nine-digit chunks. The schema, input regex, bit and
dimension caps, arithmetic, clipping, verdict comparisons and process-wide
Python digit guard are unchanged. This repairs availability without enlarging
the certificate class. Earlier results still identify the checker that ran.

The [targeted regression](format_repair_result.json) checks both large receipts
against independent Decimal-based exact round trips, five signed integer
cases, four existing receipts and rejection of an oversized witness. The
repaired lower fraction has8630 characters and returns unresolved; the
4300-digit guard is unchanged. The run took6,986,900ns after imports on
Python3.12.14; the discovering probe took2,486,800ns. Neither is independent
confirmation or an end-to-end performance benchmark.

## Assessment consequence

The mathematical soundness assessment concerns returned verdicts under
truthful premises; the defect creates no false verdict. Future confirmation
must explicitly select and hash v2 when claiming its repair, retain F1's
incompleteness, and preserve external source/bracket/edit-warrant duties.
The N16 mathematical event and75% central readiness are unchanged. The
new version does not silently replace the historical implementation.
