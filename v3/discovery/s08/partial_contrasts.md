# Source-free confidence from adaptively exposed policy contrasts

**DEVELOPMENT derivation — Codex (GPT-6), October 14, 2026 UTC.**

Fix two admitted acquisition policies i,j and a stationary sequence of fresh
independent source rows. The logging policy may change predictably using all
previous receipts. Its current partial row z supports checked paired bounds
$`L_t\le D_t=C_i(X_t)-C_j(X_t)\le U_t`$. Let the global paired range be
$`[a,b]`$ and width $`w=b-a`$. These quantities do not require a source model.

The endpoint means can depend on the logger and therefore on history.
Nevertheless $`\mathrm{E}[L_t\mid\mathcal F_{t-1}]\le\Delta\le
\mathrm{E}[U_t\mid\mathcal F_{t-1}]`$, where
$`\Delta=\mathrm{E}[D_t]`$ is fixed. For bounded martingale differences,
Hoeffding's exponential argument gives the all-time interval

```math
\overline L_t-w r_t\le\Delta\le\overline U_t+w r_t,
\qquad
r_t=\sqrt{\frac{\log(2K t(t+1)/\alpha)}{2t}}.
```

K is the number of tracked unordered pairs, and the two tails receive the
usual allocation across K and positive t. Clip to [a,b] and intersect all
previous intervals. The pointwise endpoint ordering, rather than identical
endpoint distributions, justifies the claim under adaptive logging. Exact
zero-width contrasts need no concentration. Eliminating i when a lower
bound for $`\mu_i-\mu_j`$ is positive is sound on the common coverage event.

This partial-pooling method can retain irreducible uncertainty forever. It
must supplement, not replace, the ordinary controller's exact on-policy
invoice intervals. The earlier 3/7 linear-regret counterexample applies to
naively replacing exact feedback with pooled intervals. Choose among
remaining policies by an ordinary on-policy optimistic index, and keep its
own complete-invoice samples. On the common event, eliminating a truly
minimal-mean policy is impossible; this statement alone is not a finite
regret bound for every combination of indices and confidence allocations.

Global paired ranges can be much narrower than either invoice range because
shared random components cancel. That is useful for concentration even when
the logger belongs to the pair and the conditional interval needs no joint
diagram. But if a common component is separately observable in each own
invoice, an ordinary structured controller can subtract it too. A comparison
against an unstructured noisy-bill bandit would overstate novelty and gain.

Prospective service screen: first compile the three already exposed cs01
fee vectors with the EVBDD checker, record true invoice-equivalence groups
and whole preparation bills. Only then select a bounded paid service design
based on whether those groups or contrast widths offer a plausible benefit.
Do not choose source rows or hidden labels based on a favorable contrast.
