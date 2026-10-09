# Purchased-label observable performance diagnostics

Start with [analysis.md](analysis.md) and [the complete numerical grid](full_grid.md).
Both diagnostics are offline DEVELOPMENT calculations over 20 existing
uniform and three existing adaptive episodes. No policy, service, RNG or
new private-label computation occurred.

## First prospective diagnostic

- [Public-only exact certificates](public_stage_001/result.json)
- [Public reader audit](public_stage_001/reader_audit.json)
- [Public completion seal](public_stage_001/public_stage_complete.json)
- [Later, separately invoked private-score comparison](comparison_stage_001/result.json)
- [Public calculator source](calculate_public.py)

## Separately planned centered diagnostic

- [Centered public-only certificates and exact shared correction](centered_public_stage_001/result.json)
- [Centered public reader audit](centered_public_stage_001/reader_audit.json)
- [Centered completion seal](centered_public_stage_001/public_stage_complete.json)
- [Later centered private-score comparison](centered_comparison_stage_001/result.json)
- [Centered public calculator source](calculate_centered_public.py)

The first stages deserialize only allowlisted public archive members and
selected receipts. Both close before their private-score comparison starts.
The shared [comparison program](compare_private.py) reads existing scores;
it does not recompute truth. Each stage preserves its command, source hashes,
reader events, exact Fraction values and output hashes.

[shared_identity_audit.json](shared_identity_audit.json) checks both public
seals and confirms every public centered correction equals the saved private
Brier-minus-conditional-mean difference. It also verifies all20 uniform
centered `U` values equal their originals. Its source is
[check_shared_identity.py](check_shared_identity.py).

Selected per-receipt terms and public predictable block ranges are retained
in three small ZIPs with exact member manifests. Their combined size is
897,936 bytes. No large loose JSONL was created. The original evidence
archives and scientific sources are unchanged.

The theorem premises use fresh fair randomness. The fixed seeded traces do
not establish confidence coverage. Coverage statements are per arm; the
baseline statements are separate, while the centered shared event supports
a fixed-end joint terminal/Brier statement under its stated proof contract.
No simultaneous23-arm or anytime-terminal coverage is claimed. Analysis
computation is separate from deployed invoices and principal-clock credit.

## Final two-sided public-only diagnostic

The separately saved [two-sided design](two_sided_design.md) is implemented
by [calculate_two_sided_public.py](calculate_two_sided_public.py). It reads
only the sealed centered public sufficient statistics, with no private
comparison or new run. See the [complete result](two_sided_public_stage_001/result.json),
[reader audit](two_sided_public_stage_001/reader_audit.json),
[public seal](two_sided_public_stage_001/public_stage_complete.json) and
[all23 interval rows](two_sided_grid.md).

Ten rows have Brier lower endpoints above the `T/4` null under the specified
formula; no row flags conditional-action improvement or worsening against
`(T-m)/2`. All rows and empty-intersection flags are retained; none is empty
here. The final analysis section states the per-episode/fixed-end coverage,
post-run DEVELOPMENT and unchanged-base-policy limitations. No further
analysis or scientific run is selected.
