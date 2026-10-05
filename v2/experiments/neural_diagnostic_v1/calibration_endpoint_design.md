# F15-ND01 full-endpoint constructed calibration

Contributor: ChatGPT (GPT-6 Astra Pro). Status: diagnostic development design;
no ordinary training, new confirmatory result, or F15 reclassification.

The calibration asks whether the **complete frozen search-and-assessment
endpoint** recognizes the known cost structure available in the unchanged
[compiled positive control](../calibration.py). The original F14 calibration
demonstrated known-subset accuracy; this diagnostic also applies the actual
guided search, four matched search controls, four hypotheses, scale checks,
conditional baselines, numerical checks, and the complete 560-row interval
family through the unchanged [evaluator](../neural.py) and
[assessment](../analysis.py).

Five fixed positive gauges and permutations use discovery seeds 1511601 through
1511605, stream 9000. They implement the **same constructed ordinary function**
in five coordinate layouts. They do not represent five independently learned
solutions. The direct frozen MLP initializer, seed stream 0, supplies each
untrained-network control; no optimizer or training batch is called.

The effective neural configuration equals the frozen configuration except for
these five discovery seeds and the paired diagnostic evaluation seeds 1511691
through 1511695. All hypotheses, controls, sample counts, search budgets,
thresholds and analysis settings remain unchanged. Every searched alignment is
selected without access to the construction-known subsets, using the original
128-candidate search. A favorable known-subset result cannot substitute for
the actual search endpoint.

The caller saves, hashes, reloads, and validates **all five compiled models and
all their alignments before generating any diagnostic evaluation population**.
The custom validator checks the complete searched artifact and the exact
compiled/gauged construction. It honestly records zero training; the frozen
ordinary-training validator would reject this construction and is not bypassed
with fabricated training counts.

Evaluation additionally reports the known-subset oracle's accuracy on the
exact same deterministic evaluation pairs. Regenerated pair-array hashes must
match the searched evaluation. This extra generator and oracle computation is
charged separately. Oracle accuracy receives no searched-structure claim and
does not inherit successful control comparisons from another alignment.

All five searched results enter `analysis.neural_assessment` with
`development=True`; explicit checks still require all five declared evaluation
seeds in order and the full frozen counts. Thus the original
`pilot_support_criterion_met` remains false. A separately named diagnostic field
reports whether the borrowed complete endpoint is satisfied in at least four
of these five constructed layouts. Its interpretation is endpoint calibration,
not a learned-structure result or population claim about ordinary training.

Either outcome is informative. Strong known-subset accuracy with weak searched
performance points to extraction sensitivity. Strong absolute searched accuracy
without sufficient control advantages indicates that the complete endpoint
requires more than successful recovery of useful structure. Failure on a
constructed positive control does not alone identify which component is at
fault; all component outcomes remain visible.
