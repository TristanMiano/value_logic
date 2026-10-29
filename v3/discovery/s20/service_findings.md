# Checked query and source-recovery development result

Codex (GPT-6), October 28, 2026. DEVELOPMENT; same model and exposed inputs.
The [prospective plan](range_service_plan.md), [freeze](service_freeze.json),
[driver](service_probe.py), [results](service_result.json) and exact
[source witnesses](service_witnesses.json) preserve the first execution.

The first unchanged run passed all 13 prior audit cases: 61 attainable
scalar queries returned rational sources, 28 exterior/gap queries were
rejected, and 178 band queries agreed with direct scans of the retained
exact ranges. Every returned source was checked against original base rows,
all observation bands and the new minimum by a separate direct evaluator.
This includes mixed dimensions, a 400-digit constant, degenerate slices,
no observations, one block and an inconsistent source. Caller-object
mutation after compilation did not change the retained snapshot. Invalid
certificate binding, floating query values and reversed bands were rejected.
There was no exception or retry. These finite checks do not prove the
algorithm or independently confirm the already exposed prediction sets.

The interface now makes the existing theorem's constructive promise usable.
After rechecking a complete certificate, it stores prefix/suffix subset
choices and a sorted interval-stabbing index. Membership and band queries
use O(log(m+1)) rational comparisons for m indexed intervals. Returning an
actual compatible source additionally walks O(n) split entries, performs
one affine interpolation and writes every source coordinate. Compilation,
certificate copying/storage and exact-number bit costs remain charged.
No optimization solver is called during these queries.

The conventional comparison still ties: this is an implementation of the
same ordinary LP-plus-subset construction. The new evidence closes an
interface gap between a proved witness-recovery procedure and executable
recovery; it does not establish empirical cost savings or novelty.
