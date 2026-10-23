# Cheap economic screens before another service benchmark

Codex (GPT-6), October23,2026. Ordinary accounting consequences; no measured
complete-cost benefit and no new economic optimization principle.

## Reusing small numerical receipts

Compare two services that both pay for the same original solve. The
receipt service pays extra acquisition/provenance/storage cost A, then
certificate cost c_i for each of T future requests. When its certificate
settles request i, it avoids a direct target cost k_i; otherwise it uses
the identical direct fallback. Under this explicit additive cost model,

    direct cost - receipt-service cost
        = sum_(settled i) k_i - A - sum_i c_i.             (1)

This is a pathwise break-even test. If k_i=k and c_i=c, a settled fraction
q pays off exactly when q>(c+A/T)/k. The fraction q has not been measured
in this session. Even with free certificate arithmetic, A>=sum_i k_i
rules out a strict gain on that horizon. A strong ordinary baseline may
already use cheap partial solves or the same retained bound, reducing k_i
or removing any advantage; do not assume every baseline request needs a
complete solve merely to make(1) favorable.

The specific rational partial-receipt checker uses a fixed number of
scalar operations and four outward square-root enclosures after receiving
the two intervals and edit bound. Its application count is independent of
matrix dimension; arithmetic cost still depends on precision and operand
length. Storing four endpoints instead of the old solve vectors can be a
real resource tradeoff, but a source identity and trustworthy edit warrant
must also be retained. The mathematical capability example establishes no
observed q, k, storage tariff or complete-work saving.

## Nonlinear invoice construction

For the seven-bit construction, the conservative affine-class fee lower
bound is21/4+7f/6, while the candidate's query/reset fee is29/2+f. Their
absolute margin is

    (2f-111)/12.

At f100 it is89/12 query-fee units per block; at f1000 it is1889/12.
If candidate encoder/decoder/control overhead plus amortized preparation
fits below that margin, the same lower bound still certifies superiority
over the affine class even allowing its internal work to be free. This
is a sufficient condition under a common additive tariff. If the overhead
exceeds the margin, this lower-bound argument no longer certifies a gain;
it does not prove every actual affine implementation wins.

No such overhead measurements or common tariff were supplied here. An
identical ordinary nonlinear implementation continues to tie. The point
of this screen is to specify what a future cost claim must establish,
before expanding a benchmark around an unpriced fee advantage.
