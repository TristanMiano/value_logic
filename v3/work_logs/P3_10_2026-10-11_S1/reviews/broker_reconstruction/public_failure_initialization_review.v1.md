# P3-10 public-stage deterministic initialization failure review

Contributor: **ChatGPT (GPT-6 Astra Pro)**, independent agent `/root/freeze_review`.
Observation began UTC: **2026-10-11T15:24:50.316216+00:00**. Signed UTC: **2026-10-11T15:24:50.336796+00:00**.

**Verdict: DETERMINISTIC EXECUTION BLOCKER CONFIRMED. The structural conformance adapter omits its inherited worker's explicit dependency initialization. An unchanged infrastructure retry is ineligible.**

This is a P3-10 execution-validation review. It adds **zero principal Research90 minutes**. Only the specifically authorized failure marker and source files were read. No final input, paid public result, private score or analysis was opened; no final unit, generator, scorer, observer or official verification was executed. All original frozen/live source and previous reviews remain unchanged.

## Observed failure and bound source

The retained public-stage failure marker reports attempt 1, UTC **2026-10-11T15:20:33.505276+00:00**, unit **`conformance_structural_legacy__counterpossible_tied_minima__candidate`**, exception **`AttributeError: 'NoneType' object has no attribute 'paired_request'`**. The traceback reaches `p309_conformance.run`, `p308_structural.run_method`, the metered controller/dependency-construction call, and `candidate_compile`'s `K.paired_request` access. The marker explicitly denies automatic retry and labels an unmeasured failed attempt cost as unknown unless preserved method evidence measures it.

Failure marker SHA-256: **8a218fcdd465af660962cc608dbd87ecfecc46fcd9f673a63c01a0b7e4184d12**. Its exact observed bytes are preserved in `public_failure_marker.observed.v1.json`. The accompanying JSON record binds all reviewed source bytes. Direct byte comparison found all ten selected live sources equal to their corresponding existing frozen source snapshots. This was a scoped read-only comparison, not a rerun of the official freeze verification.

## Root cause and import lifecycle

`p308_structural.py` initializes the module globals with `M = K = None`. Its `_load_legacy()` function is the operation that loads `05_counterfactual_transport.py` and assigns `M` and `K = module.K`. The transport module imports or reuses its own inherited `04_counterfactual_repair.py` dependency.

The original `p308_structural.run_development()` explicitly calls `_load_legacy()` before fixtures and paid method runs. Static AST inspection finds `run_development` as the sole caller of `_load_legacy` within that module, and no caller anywhere in `p309_conformance.py`.

The adapter's `_load()` only executes the structural module's top-level definitions and caches that module in its own deterministic `sys.modules` namespace. `generate()` calls `legacy.fixtures()`. `_bound_inputs()` independently calls the same fixture constructor and checks the known definitions. Neither fixture construction nor input binding initializes `M` or `K`. `run()` then calls `legacy.run_method()` immediately after loading the same uninitialized module. `run_method()` does not initialize it either. The first candidate paired fixture reaches `K.paired_request` and raises the observed exception.

**This is not merely a loss of initialization between separate input and public processes.** The shown input-generation path never performs the required initialization. Combining the two stages in one process would still fail unless some other code explicitly primed that exact structural module instance. Priming an independently imported transport/kernel module elsewhere does not assign the structural module's `K` global. Each official stage starts a fresh command-line process, so any incidental state from preparation or a prior stage would in any case be unavailable.

The preparation selfcheck tests conformance exposure barriers, information-audit development toys and rejection of a structural budget below admission. It does not invoke an admitted structural `run_method` or assert the legacy globals are initialized. Its successful scope therefore does not test this missing lifecycle prerequisite. The earlier static freeze/barrier PASS is preserved; it was not evidence that every admitted final worker path had executed successfully.

## Tariff placement and the lost prefix

The inherited driver initializes dependencies before constructing the paid worker account. The declared structural tariff uses source-byte enrollment for supplied code and excludes interpreter bootstrap. A minimal initializer in the adapter immediately before `run_method`, outside the meter, is consistent with that original placement. Moving dependency imports into `candidate_compile`, a metered lambda, or another paid worker function would change the traced workload and would require a larger tariff/amendment assessment.

The actual failure is after `deployment_setup` admitted source bytes and input bytes, and after storage/controller/dependency-construction work began. `run_method` catches only its typed `ResourceExhausted` exception. The observed `AttributeError` escapes before the function returns its invoice and before the outer lifecycle publishes the unit result or seal. Thus the failed prefix contains paid work, but these authorized observations provide no exact authoritative total. The source and traceback establish that zero is inappropriate; they do not recover missing event counts. This cannot be relabeled a budget failure or a completed negative semantic score.

The frozen `execution_history` regards an unsealed public attempt as having unknown cost. The frozen analyzer applies `complete_outer_paid_attempt_accounting` globally: it suppresses broker positive-price practical catalogue flags, broker equal-output cost-saving flags, priced paired effects at positive price, and certificate practical cost dominance. Completed-path threshold diagnostics remain distinct. That conservative global gate cannot be narrowed to ignore conformance, or set true, while claiming the unchanged frozen analysis. The conformance tariff also must not be arithmetically added to an incompatible broker/certificate tariff to invent a missing combined invoice.

## Affected-data scope

The following completion counts are the principal's reported execution state, not an independent read of final results. The scheduled conformance counts and the first-case ordering are independently present in the source.

| Portion | Scheduled units | Current disposition and scope |
|---|---:|---|
| Broker | 336 | Principal reports sealed before this defect. Preserve their original input/result/seal bindings. Their scientific validity is not established by this source review and remains unscored. No direct path from the later structural initialization failure to their already sealed values was found. |
| Certificates | 104 | Principal reports sealed before this defect. The same preservation and unscored qualification applies. |
| Structural conformance | 18 | The first candidate invocation failed. The remaining 17 units are not reported executed. The missing kernel is directly needed by all nine candidate fixtures; the nine ordinary paths use their independent compiler/solver/checker. All 18 still belong to an unfinished paired conformance panel. |
| Information conformance | 42 | Reported unstarted because the earlier exception stops the sequential stage. Its independent audit path does not use this structural `K`; no direct semantic effect from this defect is established. It remains required by the public denominator. |

The complete original public denominator is 500. The retained 440 completed method records cannot make a 440-unit subset into a complete frozen public stage. `final_stage` calls `public_stage.verify_complete()` before any private scorer, so evaluation and analysis must remain blocked under the original lifecycle. No late private scoring of only the completed arms is authorized by its barrier.

All affected regenerated or amended conformance results are post-exposure results. This conformance panel was already explicitly classified as regression/conformance, not unseen transfer. The amendment must still identify its repair and retain the original failure. The original broker and certificate acquisitions may be cited as original frozen records if later validated; a combined post-amendment report must disclose its mixed provenance and cannot describe the failed original v1 stage as having completed unchanged.

## Minimal versioned amendment proposal

The minimal semantic correction is a call to the already present initializer at the structural adapter boundary:

```python
legacy = _load("v3/experiments/p308_structural.py")
legacy._load_legacy()  # explicit interpreter bootstrap before the paid account
inner = legacy.run_method(selected, unit["worker_method"], budget=config["structural_budget"])
```

This is a proposal only; no source was edited or run. The worker, candidate/ordinary algorithms, tariffs, fixture roster, budgets, seeds, public inputs and scoring definitions can remain byte-for-byte unchanged. A versioned wrapper or copied adapter can supply the call while retaining original frozen source. It should initialize the exact module instance that executes `run_method`, idempotently in each fresh public worker process. The private structural checker shown here uses `ordinary_compile`/`solve_ordinary` and does not require candidate `K`; no gratuitous scorer change is needed for this error.

The small source change still requires an explicit amendment record. At minimum, the amendment needs its own identifier and source/entrypoint hashes, the original freeze/protocol/failed-marker bindings, the single behavioral change and tariff justification, a precise affected-unit roster, and the post-exposure evidence label. It must preserve every original exposure/start/failure/result/seal and the unknown failed-prefix cost. Any reuse of the 440 sealed records must be by immutable original references, not by editing their identities or generating replacement method outputs.

The current `Stage` and `final_stage` implementations provide no deterministic-amendment execution command: a subsequent public attempt requires `unexplained_infrastructure`, and every stage/result/seal is tied to its original manifest binding. Therefore an amended continuation needs an explicitly versioned execution/provenance mechanism that retains the full 500-unit public-before-private barrier and the original seals' lineage. If a separate amendment namespace or output root is chosen, that deviation must be named by the amendment itself; the frozen protocol does not offer a silent root-switch option. In-process monkeypatching followed by original-looking v1 seals would conceal the execution change even if the source files on disk were unchanged. A fresh seed, deletion, altered marker, relabeled infrastructure retry, or silent overwrite cannot serve as the repair.

Before any amended final execution, a fresh-process initialization smoke check on the versioned entrypoint can verify that the exact worker's `M`/`K` are populated and correctly sourced without replaying a final fixture. Preparation records and source checks should be retained. A successful smoke check would close this particular initialization prerequisite; it would not establish future public outcomes or relax the barrier.

## Outstanding work

The principal must choose and record the versioned deterministic-defect disposition. This review does not authorize or execute it. Broker reconstruction and the continuous-price observer remain on hold because public/evaluation/analysis have not completed and no final-data release has been given. The broker observer remains SHA-256 **4f3ca8a9fc52edd3fdf6de4075b4d6c424c0624f10103de6f7222851b1f9a75f**.
