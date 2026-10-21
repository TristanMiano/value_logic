# Price uncertainty as a separate information constraint

Codex (GPT-6), DEVELOPMENT, October20,2026. Cheap constructive screen;
no empirical application or new numbered family. Lineage: invoice readout,
fallible cost models and paid calibration.

The unit-count interface assumes the invoice identifies the number of queries.
It need not require knowing every individual query price. Suppose every
actual query, even with adversarial variation across calls, costs in[a,b],
where0<a<=b are justified bounds. A j-query episode has bill in[ja,jb].
These intervals are pairwise disjoint through cap H if

```math
\frac ba<\frac H{H-1}.
```

Indeed the hardest adjacent separation is (H-1)b<Ha. Thus the public observer
can recover the exact query count and execute the existing prefix or
parity-prefix decoder without calibrating each coordinate's tariff. The
price bounds are a physical/interface premise, not learned for free.
With a known fixed reset price f, subtract it before decoding. An unknown
reset price would need a separate bound or paid reference observation.

The worst expected query-plus-reset bill of a fixed protocol over all
admissible price paths is attained when every query costs b. Therefore the
new rate theorem supplies a minimax asymptotic upper and lower coefficient
b*beta(H,f/b) when exact count decoding is possible. The lower bound uses
the allowed constant-b tariff; the upper bound uses the per-query ceiling.
This is a robust tariff adapter, not optimality for arbitrary ambiguous
price intervals. Choosing a smaller effective cap may restore disjointness.

At equality or beyond, interval overlap means counts alone are no longer
universally identifiable from one bill. For cap2 with b>=2a, a one-query
branch billed2a and a two-query branch billed a+a have the same invoice.
Even exact real readout cannot distinguish them. For higher H, overlapping
adjacent intervals provide the analogous arithmetic ambiguity. This rejects
the naive count-decoder, not every adaptive protocol or every fixed-price
model. Stable coordinate prices can be learned by unconditional single-query
episodes whose bills reveal prices without revealing their Boolean answers;
that calibration purchase belongs in the total, and may itself cost more
than the intended information gain.

This is standard separation of uncertain cost alphabets. Keep the lemma as
an interface robustness condition; do not build a new benchmark merely to
rediscover robust coding or turn an assumed tariff interval into evidence
that a noisy physical timer satisfies it.
