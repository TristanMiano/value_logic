# A cheap rejection of same-price guidance for range discovery

Codex (GPT-6), October23,2026. DEVELOPMENT; generation pass16.

Suppose arbitrary guided probes are interleaved with the uniform F2 probes
of error_scope.md. Every acquired vector is a genuine E*u and added to the
retained span. Only redundancies among the uniform probes count toward the
statistical stopping threshold h. Guided outputs are never silently treated
as uniformly sampled points.

The old failure upper remains valid: at missing rank j, a fresh uniform
probe is redundant with probability2^(-j). Guided rank increments can skip
some waiting stages but cannot create extra uniform failures at a fixed
rank. Couple their failure counts with the usual geometric waiting counts
for ranks d,...,1. The total before completion is stochastically no larger.

However this does not give a query-count improvement. On a correct stop,
let g be the number of guided probes and r_g their rank increments. Uniform
probes supplied d-r_g increments and exactly h redundancies. Total probes
are

    g+d-r_g+h >= d+h,

because r_g<=g. The unguided procedure itself uses exactly d+h probes on
a correct stop. Thus a same-price one-vector-per-probe guidance scheme
cannot beat this count while retaining this stopping rule, even with an
excellent forecast. It can only help if probe costs differ, one paid
computation supplies several warranted vectors, or a new kind of receipt
changes the certification requirement. These are new premises to price.

Counting guided redundancies as uniform evidence would invalidate the
argument: a guidance rule can keep querying a known kernel vector forever.
No benchmark of that unsound shortcut will be built. Known rank upper bounds
can also remove some random verification work, but acquiring such a bound
is a separate duty, not a free benefit of model confidence.
