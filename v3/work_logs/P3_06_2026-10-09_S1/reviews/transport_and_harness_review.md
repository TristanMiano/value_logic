# Independent transport and mathematical-query review

Contributor: **ChatGPT (GPT-6 Astra Pro), independent implementation reviewer**.
October 9, 2026 UTC. All executable evidence in this review is development;
reviewer effort is not added to the principal Research90 clock.

**Disposition:** the transport mathematics and the recorded query chronology
are sound within their stated scope. A material receipt representation defect
was found, preserved, repaired in harness v3, and independently rechecked.
The valid numerical trajectories and their metrics did not change.

## 1. Transport argument and probe correspondence

The [transport manuscript](../../../derivations/06_forecast_transport.md) and
its [probe](../../../checks/06_forecast_transport_probe.py) describe the same
mathematical objects.

For CF-8, use equally frequent contexts with deterministic answers zero and
one. Conditional report distributions assign probabilities $`(3/4,1/4)`$ and
$`(1/4,3/4)`$ to reports $`(1/4,3/4)`$. Aggregating across contexts gives the
correct answer frequency at each original report value. Replacing these
distributions by their context means produces reports $`3/8`$ and $`5/8`$,
whose answer frequencies are zero and one. The conditional errors are therefore
$`-3/8`$ and $`3/8`$.

There is no chronological requirement that a deterministic mathematical answer
be independent of its visible context. The counterexample uses a declared
report distribution before selecting its random report. Its finite eight-report
version is an exact realization with those counts; it does not claim that every
independent draw has exact finite calibration. Its premise is calibration by
report value across the contexts, not calibration separately within every
context. Squared-loss improvement under taking the mean is compatible with
this failure of calibration transfer.

For CF-9, the local square-loss difference factors as

```math
|(p'-y)^2-(p-y)^2|=|p'-p|\,|p'+p-2y|\le2|p'-p|.
```

Nonnegative weights allow summation, and the unchanged expert tape cancels in
the regret difference. For a test bounded by one with Lipschitz constant
$`m`$, adding and subtracting $`b(p)(y-p')`$ gives exactly the manuscript's
$`(m+1)|p'-p|`$ local bound. The tent tests satisfy the required magnitude and
Lipschitz hypotheses. Neither argument identifies the forecast tape of a
different stateful training run.

The fixed-grid statement must describe an upper allowance, not a lower bound
on actual error: already-on-grid reports have zero displacement. This wording
was communicated to the principal and corrected in the manuscript.

For the common outcome-dependent offset, keep the issue weights, smoothing and
other learner settings fixed. Adding $`M_ty`$ changes both slopes by the same
amount, leaves their difference and the forecast cost difference unchanged,
and cancels from both relative decision coordinates. The cost-level error
identity concerns **signed error**:

```math
(\widehat c'_t-c'_t)-(\widehat c_t-c_t)=M_t(p_t-y_t).
```

It is not an additive identity for absolute error magnitudes. The probe checks
this signed identity, including positive and negative common coefficients.
The distinction between error in an absolute cost estimate and the absolute
value of an error was communicated to the principal and is now explicit in
the manuscript. The underlying algebra required no change.

## 2. Independently reconstructed saved chronology

[`audit_saved_chronology.py`](../development/independent_harness_review_v1/audit_saved_chronology.py)
and its [`result`](../development/independent_harness_review_v1/saved_chronology_result.json)
pass **6,241 checks** on the original saved run. They validate file hashes,
immutable report hashes, exact modular residues, event bindings, admission
timing, cache provenance and scores. Each expert vector is rebuilt using only
the inputs and answers already admitted at that point in the event sequence.

| Original development case | Fresh forecasts | Cached requests | Fresh admitted answers | Pending requests |
| --- | ---: | ---: | ---: | ---: |
| Recurring shortcuts | 127 | 1 | 127 | 0 |
| Balanced nonshortcut null | 127 | 1 | 127 | 0 |
| Delayed pending tail | 127 | 1 | 119 | 8 |
| Varying stakes and actions | 127 | 1 | 127 | 0 |

Every unknown request commits all reports before its recorded repeated-power
production and independent check. Admission follows checking and occurs on
the announced end-of-tick schedule. Private pending receipts are present in
the reproducibility archive but are absent from admitted expert history and
public scores. This assessment uses the actual tape and runner discipline;
it does not claim that any arbitrary externally constructed simulator history
is validated by a single receipt method.

Cached requests deliberately lie outside the online learner's copy history
while appearing in the public metrics. This is mathematically consistent:
their forecast and all cache-wrapped experts equal the known answer, so they
add zero Brier loss, zero expert regret and zero calibration residual. Their
exact chosen action adds nonpositive regret against each fixed action. The
unknown-round upper certificates therefore extend to the combined metrics.
The public metric weight equals core settled weight plus cached weight.
Including solved repeats in a normalized score is not evidence of improved
performance on fresh claims.

## 3. Ordinary-comparison fairness

The ordinary K29 rows share their scalar counterparts' numerical core and
report tape intentionally. They demonstrate equivalence of the adapters, not
independent validation or an advantage over ordinary forecasting.

The AA receives the same expert vectors, positive weights, cache channel and
admitted feedback, with the same free-copy scheduling rule. Its binary scalar
loss is half the vector Brier loss in [Vovk and Zhdanov (2009), Section 2,
Algorithm 1 and Theorem 1](https://www.jmlr.org/papers/volume10/vovk09a/vovk09a.pdf).
The implemented fixed exponent-update rate is $`2/w_{\max}`$, with current
scalar rate $`2w_t/w_{\max}\le2`$. Binary substitution reduces to
$`p=(1+g_0-g_1)/2`$ with clipping where needed.

An independent 80-digit Decimal replay reconstructed the AA from the admitted
event tape. The largest difference from any recorded binary64 probability was
less than $`4.47\times10^{-15}`$. This is a numerical diagnostic, not an
interval-certified mixability bound. The exact solver has the full public
arithmetic input, pays for its own modular computation and is not artificially
prevented from solving fresh queries. Its results are not passed into the
learning methods before admission.

The generator intentionally uses exact arithmetic to create the synthetic
query population and exposes its selection rule. The “null” case is therefore
relative to the small supplied heuristic library, not computationally hard
against arbitrary ordinary methods. The report correctly retains this
limitation and the exact solver's zero-loss result.

## 4. Receipt failure, repair and independent recheck

The frozen pre-repair harness has SHA-256
`c4dcb0ffafc74e888f434af8009bec19a6632a240461b5bb3cfd341634473e04`.
Its negative evidence is preserved in the
[`boundary reproduction`](../development/independent_harness_review_v1/reproduce_receipt_boundaries.py)
and [`failure record`](../development/independent_harness_review_v1/receipt_boundary_failures.json).

Python dataclass equality treats integer one, Boolean true, floating one and
`Fraction(1)` as equal. Replacing an integer answer by one of these aliases
produced an equal registry record but a different serialized digest. Evidence
admission accepted it and changed the cache; the forecasting core then rejected
the noninteger answer, leaving its original prediction pending. Separately,
mutable counter dictionaries inside the ostensibly frozen receipt allowed a
returned receipt's digest to change while remaining accepted. A control probe
confirmed that a wrong ordinary integer answer was already rejected. These
failures do not imply false integer labels in the valid saved tapes.

The owner preserved the prior source/results and introduced strict receipt
field types, canonical immutable counter tuples and a separately stored digest
captured at registration. The reviewed v3 source has SHA-256
`7e19e1e0930cbcdea3637af16c1ade4e1f2099b615a3600821196c2c8c5cecd4`.

[`check_receipt_repair_v3.py`](../development/independent_harness_review_v1/check_receipt_repair_v3.py)
and its [`result`](../development/independent_harness_review_v1/receipt_repair_v3_result.json)
pass all **26 malformed-candidate and tick probes** without changing complete
evidence or core fingerprints. Live counter mutation fails. A canonically
identical reconstructed receipt is accepted afterward; duplicate admission is
rejected; and the admitted residue answers new same-scope target requests
correctly. The full 6,241-check saved-tape audit also passes on v3.

The old and repaired runs have exactly the same query population, prices,
action tables, expert tape, issued forecasts, pending population and every
reported metric. Only representation, integrity checks and associated
receipt digests are versioned. The repair does not create an external
authentication service or a global transaction across independent consumers.

No historical evidence, principal clock, phase status or gate decision was
changed by this review.
