# Exact capped intervals: accepted formal contraction

Codex (GPT-6), October 28, 2026. Supplemental P3-11-A1 evidence.

The second retained attempt accepts [Capped.lean](Capped.lean), exit 0 in
1426282700ns. The [first deterministic proof-term failure](capped_repairs.md)
is preserved. The [accepted record](capped_attempts/a02.json) and
[seal](capped_seal.json) identify all dependencies and attempts. Execution
was excluded from engaged research.

`anchored_capped_iff` replaces each anchor's existential outside assignment
by one maximizing assignment and its bottleneck cap. No feasible assignment
produces no interval; a feasible empty outside family is handled correctly.
The proof uses a finite ceiling M above every local upper endpoint in place
of infinity. Every anchor value is already <=M, so clipping to its own upper
endpoint makes this convention equivalent. Finite local tables supply such
an M by taking their maximum, including arbitrary inactive default endpoints.

Composing this with `finite_complete_certificate_image` gives the exact
closed-interval union from original affine premises and complete certificates.
For n blocks and k receipts there is at most one interval per (i,T), hence
at most n*2^k before merging. The upper endpoint is the minimum of the local
upper value and the greatest feasible outside cap. The supplied maximizing
assignment attains the cap, which also supports source reconstruction.

The formal cap is defined using a complete finite assignment list. This is
a specification of the value, not the efficient implementation. The written
prefix/suffix subset recurrence and the separately sealed monotone argmax
compression lemma justify its efficient computation. The Python bitmask loop
and the asymptotic operation counts are not machine verified here. No claim
of enumerating n^k assignments within the n*3^k bound is made.

The five printed new lemmas depend only on propext, Classical.choice and
Quot.sound. No frozen scientific statement or candidate code changed.
