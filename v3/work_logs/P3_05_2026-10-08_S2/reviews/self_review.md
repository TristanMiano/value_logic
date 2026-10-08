# P3-05 reconstruction self-review

Contributor: ChatGPT (GPT-6 Astra Pro), October 8, 2026 UTC.
Scope: this new reconstruction, not a missing independent review.

## Load-bearing checks

CT05-1 requires current nonemptiness and a valid mapped proof for every new
winner. The formula chooses a proof, not a hidden-state-contingent action.
CT05-2 needs only a feasible incumbent, not an optimality oracle. Its cutoff
inequality includes equality, hence retains ties. With rank perturbations the
2-epsilon endpoint is sharp; without rank/loss linkage it bounds no loss by
itself. The explicit turnover example both succeeds and fails under different
hard restrictions. CT05-3 requires the operation-commuting map for intervention
claims; extensional baseline equality alone is insufficient.

The current v2 split verifier checks both children, rejects repeated splits,
recomputes each leaf, and binds the entire old request. The cache receives only
verified immutable data through its supported API. The substitution map is
checked Boolean, mapped old hard premises are rechecked, the new seed is
verified, and the rank/loss bridges are computed independently of advertised
bounds. A removed q=0 premise needs a four-unit loss penalty in the worked
example. No silent old-assumption or optimistic tie reuse was found in these
checks. The conclusion is a conditional hand proof plus finite development,
not mechanically checked universal soundness.

Canonical JSON record comparison distinguishes true from integer 1, and rejects
duplicate keys and metadata floats. This corrects the new receiver's own
potential Python-equality hazard without changing any historical P3-04 code.
Private cache corruption and arbitrary malicious Python object behavior are
outside the finite immutable input contract. A digest by itself is never used
as a proof or full-record identity.

## Evidence provenance

Five fresh bundles exist: v1 main and extension; v2 substitution, main regression
and extension. Each has a pre-execution manifest, complete exact sources,
results and a summary. The finite point oracle is separately implemented by
the same contributor; no different researcher, agent or external validator
was available. The unchanged P3-04 dependency matches Git blob
`2c4f69fb756c4c84917a560245f44d41adc4cb3e`. No source from the lost P3-05
attempt was recovered or relabelled.

## Limits that are still informative

The source-preserving checks are sufficient, not complete. The rank bound
ignores some relations between formulas. Current feasibility discovery is not
free merely because a witness is supplied to the receiver. Proof generation
may be exponential. Cached matching can cost more than a trivial direct proof.
The parity fixture demonstrates operation savings for the implemented methods
but admits a strong ordinary symbolic shortcut. Cost counters are partial
heterogeneous instrumentation; measured submillisecond timings are not a
statistically robust performance result. Native proof compilation, comprehensive
portfolio selection and unrestricted semantic equivalence remain separate.

No general logical-learning, calibration or non-exploitation result is claimed.
The relevant progress is toward C01-C03, R01, I01 and action-quality/resource
interfaces. A guarded rank-envelope can preserve a task certificate after
optimizer turnover; this is more specific than just caching an old best number.
Prior work already supplies incremental analysis and optimization, so the
proposed cross-component service still needs its comparison scope assessed.
P3-N01 remains NOT YET SUPPORTED; no gate is passed by this review.
