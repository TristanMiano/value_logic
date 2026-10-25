# Prospective ordinal path and cut screen

Codex (GPT-6), s18 DEVELOPMENT. This new checker is separate from the frozen
Kemeny probe. Check raw-count and winning-edge strongest-path orderings with
an exact small adversary over available subsets and feedback, including ties,
unknown actual corruption counts, and the improving-feedback variant.
Use d<=3, horizon<=9, corruption budgets<=2; do not interpret finite maxima
as a sharp general bound. Compare max-min closure with simple-path enumeration.

For report cuts, compare an integer augmenting-path max-flow implementation
against exhaustive binary countermodels, and on small cases against all
utilities with d possible ordered levels. Include winner stars whose
comparisons share one fault, the disjoint-path warrant, the four-vertex
update-summary obstruction, and the known set-cover/label-cut reduction.
Record exact cases and operation counts; no wall-clock speedup or novel
max-flow algorithm is claimed. Preserve failed runs instead of overwriting.

The frozen [checker](ordinal_check.py) passed once on Python3.12.14 in
4,004,863,900ns. SHA256:
d9ae1adfa025b3ae7e7e9ad9613b29064caa4996b5e9020f191729f1f90da154.
The [result](ordinal_result.json) records160 path-matrix crosschecks,
490,498 adversary states and3,090,533 transitions,140 report graphs with
1,400 cut queries (280 also checked over all ordered utility levels), and
109 set-cover reductions. The shared-report fixture has cut1, while two
independent paths have cut2; current all-pair cut values6 evolve to6 and8
under the same update. All tested bounds and identities held. These checks
support the stated finite contract, not novelty or a practical speed claim.
