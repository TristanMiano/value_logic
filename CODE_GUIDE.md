# A plain-language guide to the code

This guide explains what every Python, C++, header, and CMake file in this repository does, why it exists, and how the pieces fit together. It is written for readers who are comfortable running a command but do not need to know machine learning, formal logic, or C++.

The repository is a research prototype, not an installed application. There is no graphical interface or web server. Most code either:

1. turns a mathematical claim into a small, checkable example;
2. tests that the example behaves as claimed; or
3. runs the preregistered neural-network experiment.

The mathematical explanations remain in [`formalism/`](formalism/), [`ml/`](ml/), and [`experiments/`](experiments/). The code is an executable companion: it catches mistakes and supplies finite witnesses, but it is not a proof assistant and does not make a theorem true merely by passing a test.

## The project in one picture

```text
Mathematical design
  formalism/*.md and ml/*.md
          |
          +--> small executable meanings and examples
          |      verification/*.py
          |                |
          |                +--> verification/test_*.py
          |
          +--> frozen synthetic experiment
                 protocol.py creates artificial "worlds"
                              |
                 implementation.py turns worlds into features
                              |
                 learner.py trains matched ReLU networks
                              |
                 held-out calibration expands uncertainty intervals
                              |
                 repaired_evaluator.py evaluates numeric blocks
                              |
                 cpp/value_logic_kernel.cpp decodes exact logical states
                              |
                 run_repaired_experiment.py saves checkpoints and results
```

The C++ function does not replace the Python experiment. It performs one compact, repetitive decoding step for large numeric blocks. Python still owns world generation, neural-network training, calibration, metrics, checkpointing, and the command-line interface.

## A few terms used by the code

- **Atom:** one requirement, such as “the model's loss is below this threshold” or “the candidate improves on the fallback.”
- **`Refuted`, `Open`, `Supported`:** the three meaningful states of an atom. `Open` means the available accepted evidence does not settle it; it is not the number zero and is not a synonym for false.
- **Well-formedness (`WF`):** whether the request itself supplies all required identities, scopes, profiles, and diagnostic records. A malformed request is `Undefined`; that is separate from an atom being `Open`.
- **Profile:** the list of atoms required for a particular kind of license.
- **License:** permission to rely on a plan for a specified task and domain under a specified profile. It is not a declaration of universal or final truth.
- **Plan:** a candidate method or model that can be used. A plan can itself be a directed acyclic graph (DAG) made from smaller computations.
- **Fallback:** what happens if no candidate is licensed, such as retaining the status quo.
- **World:** one deterministic synthetic test case. Different experimental roles use disjoint sets of worlds.
- **Structured arm:** the network predicts numerical centers and interval widths; calibration and an exact decoder then determine logical states.
- **Cross-entropy arm:** the comparison network directly predicts one of the three atom states, subject to the same external evidence and polarity checks.
- **Active mask:** the exact list of currently licensed candidates. The router may select only from this list.
- **Positive surplus:** the amount by which one named, accepted comparison clears a boundary. It is useful downstream, but it is not by itself a full license.

## First-time setup

Run commands from the repository root. The experiment's pinned Python dependencies are listed in [`experiments/requirements.txt`](experiments/requirements.txt).

On Windows PowerShell, one typical setup is:

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r experiments/requirements.txt
```

The repaired evaluator also needs CMake and a C++17 compiler. The tested Windows toolchain is Visual Studio 2022 with the “Desktop development with C++” workload. The native build is local and disposable; it goes under `.cache/` and is not committed.

## Common safe workflows

### Check the repository without running a scientific experiment

```powershell
python -m verification
```

This discovers and runs every `verification/test_*.py` test. It checks the semantic examples, repository links, experiment contracts, Python/C++ agreement, and authorization guards. It may compile the local C++ test library under `.cache/`, but it does not authorize final-confirmation data generation.

To check only Markdown links:

```powershell
python -m verification.check_links .
```

### Build and test only the C++ decoder

```powershell
python -m experiments.build_cpp_kernel --verify-debug
```

This configures, builds, and tests both the optimized and debug forms of the small decoder. It does not train a network or generate experimental worlds.

### Check the repaired experiment without using production data

```powershell
python -m experiments.run_repaired_experiment --preflight
```

This verifies frozen source hashes, exercises the C++ decoder, compares the repaired and original Python paths on pilot-role cases, checks the final-data embargo, and runs the deterministic system witness.

The bounded repair pilot is also non-confirmatory:

```powershell
python -m experiments.run_repaired_experiment --pilot
```

It uses pilot-role worlds, performs small fits and differential checks, and estimates whether the repaired path is fast enough. It is an engineering check, not evidence for or against the scientific hypotheses.

### Commands that performed the registered experiment

Task 21 used four separately checkpointed stages:

```powershell
python -m experiments.run_repaired_experiment --task21-select PREPARE-VALUE-LOGIC-REPAIR-V1-1
python -m experiments.run_repaired_experiment --task21-fit PREPARE-VALUE-LOGIC-REPAIR-V1-1
python -m experiments.run_repaired_experiment --task21-calibrate PREPARE-VALUE-LOGIC-REPAIR-V1-1
python -m experiments.run_repaired_experiment --task21-confirm RUN-VALUE-LOGIC-REPAIR-FINAL-V1-1
```

These are intentionally not general “try it” commands. Task 21 has completed, so **do not run them again**. The first three create production training, model, and calibration artifacts. The last command crosses the final-test embargo and evaluates untouched confirmation worlds. The exact tokens make accidental execution less likely; they do not replace the project author's authorization. The runner also refuses to overwrite a verified completed run.

The completed local raw result can be reanalyzed without generating a world, fitting a model, or crossing the final embargo:

```powershell
python -m experiments.analyze_results
```

This reads and hashes the existing raw/checkpoint/trace artifacts, applies world-first paired inference, and deterministically rewrites the compact analysis and three figures. It cannot reconstruct a missing raw run. See [`experiments/02_results.md`](experiments/02_results.md) for the plain-language result.

The older `python -m experiments.run_experiment --task21-final ...` entry point is the original all-at-once v1 path. It is retained for provenance and differential comparison. The repaired, resumable v1.1 entry point is the operational path.

## The verification code

The files under [`verification/`](verification/) use mostly Python's standard library. They are deliberately small and explicit so the semantics can be inspected without understanding PyTorch. Most are libraries imported by tests rather than commands run on their own.

### Semantic implementations

| File | What it does | Why it is needed |
|---|---|---|
| [`verification/__init__.py`](verification/__init__.py) | Marks the directory as a Python package and exposes the two most common enums, `AtomValue` and `Outcome`. | Lets other files use stable imports such as `from verification import AtomValue`. |
| [`verification/__main__.py`](verification/__main__.py) | Discovers every `test_*.py` file and runs it with `unittest`. | Provides the single `python -m verification` health-check command. |
| [`verification/kernel.py`](verification/kernel.py) | Defines the compact reference semantics: intervals, three atom values, four public outcomes, profiles, plans, contexts, requests, provenance, diagnostics, well-formedness, finite meet, and atom/request assessment. | This is the executable meaning of the paper's central `WF + K3` logic. It keeps malformed requests separate from meaningful uncertainty and preserves the witness or obstacle behind every state. |
| [`verification/witness.py`](verification/witness.py) | Builds one complete three-stage example (`t0`, `t1`, `t2`) with old and new plans, overlapping domains, fallbacks, dominance comparisons, bridges, evidence updates, lapse, rebuttal, retention, routing, and provenance. The ready-made object is `WITNESS`. | A concrete example makes the abstract rules jointly checkable and shows that the individual sections form one system rather than unrelated definitions. |
| [`verification/footprints.py`](verification/footprints.py) | Names the exact record keys read and written by adequacy, improvement, trace, and comparison clauses. It includes “negative reads,” such as checking that no dominating record exists. | An update can matter by adding a record that was previously absent. Explicit read/write sets let tests show when an update can or cannot change an assessment. |
| [`verification/encodings.py`](verification/encodings.py) | Implements finite checks for dependency-scoped inputs, shared scoring over candidate libraries, sparse comparison counts, typed plan-DAG isomorphism, and consumer-relative encoding sufficiency. | It prevents a neural encoding from silently omitting information needed by a declared downstream consumer or tying meaning to arbitrary candidate order. |
| [`verification/relu_architecture.py`](verification/relu_architecture.py) | Provides scalar ReLU helpers and a small hybrid decoder for learned centers/intervals plus exact evidence gates. It also demonstrates named dual-use surplus channels and exact active-mask routing. | It makes precise the limited meaning of a positive or zero ReLU value. Favorable learned scores cannot bypass evidence, polarity, boundary, profile, or fallback rules. |
| [`verification/representation_theorems.py`](verification/representation_theorems.py) | Supplies finite computational witnesses for representation claims: observation partitions, robust margins, ReLU max constructions, piecewise-affine seams, candidate-library limits, dual-use codes, and proof-erased CPWL plan evaluation. | It tests the boundary of what a fixed vector/ReLU representation can preserve and records counterexamples to overly strong claims. |
| [`verification/policy_value_reconstruction.py`](verification/policy_value_reconstruction.py) | Implements the Task 22B finite policy/action-score contract, exact canonical round trip, oracle disagreement terms, conservative gap decoder, scalar-value decision harness, stochastic metrics, IID disagreement bound, and trajectory union bound. | It keeps exact representation existence, raw behavioral recovery, accepted certification, return semantics, and sequential scope as separately inspectable objects. |
| [`verification/losses.py`](verification/losses.py) | Implements the small reference versions of interval scoring, schema-balanced structured loss, calibration residuals and radii, exact decoding, atom cross-entropy, router loss, risk/coverage metrics, normalized surplus, and split-disjointness checks. | It states what the networks are being optimized to do and keeps training convenience separate from the exact rule that grants or withholds reliance. |
| [`verification/proof_plans.py`](verification/proof_plans.py) | Represents a typed computation as a finite DAG. It can run the plain computation, run it while building a certificate, verify that certificate, propagate error/resource grades, trace evidence to grounded sources, and evaluate a lower-to-higher-rank assessment graph. | This is the executable answer to whether programs can both compute and carry checked adequacy information. It also blocks circular self-support in the supported finite fragment. |
| [`verification/check_links.py`](verification/check_links.py) | Finds local Markdown links and GitHub-style heading anchors, reporting missing files or anchors. External URLs are ignored. | Research repositories accumulate many cross-references; a broken link can make an otherwise correct argument difficult to follow. |

### Verification tests

Each test file is part of the full `python -m verification` run. A passing test is a regression check or a finite witness, not an empirical discovery and not a machine-checked proof of every possible case.

| File | What it checks in plain language |
|---|---|
| [`verification/test_kernel.py`](verification/test_kernel.py) | The three atom states combine correctly; the four public outcomes are derived from well-formedness plus atom states; diagnostics remain complete and value-indexed; missing evidence is not confused with a malformed fixture; interval boundaries and comparison searches use the intended rules. |
| [`verification/test_witness.py`](verification/test_witness.py) | Every stage of the integrated example: simultaneous use, route choice, resource/fallback arithmetic, supersession, comparative profiles, domain splitting, bridge statuses, lapse versus rebuttal, empty active sets, and append-only correction provenance. |
| [`verification/test_metatheory.py`](verification/test_metatheory.py) | Finite cardinality and separation examples behind the profile/status metatheory, including which status vectors remain possible under refinement. |
| [`verification/test_transport_routing.py`](verification/test_transport_routing.py) | Subdomain error, exact hard-router decomposition, routing penalties, bridge/blend risk, plan-DAG error propagation, and the cycle condition for consistent additive bridges. |
| [`verification/test_audit_repairs.py`](verification/test_audit_repairs.py) | Negative collection-index reads, candidate/fallback dependencies, future comparison writes, projection invariance, and the fact that licensed components do not automatically license a composite plan. |
| [`verification/test_encodings.py`](verification/test_encodings.py) | Dependency projections, explicit missingness, candidate permutation symmetry, sparse versus dense comparisons, typed DAG renaming, checker identity, and counterexamples showing why an adequacy scalar alone can lose payload information. |
| [`verification/test_relu_architecture.py`](verification/test_relu_architecture.py) | Paired ReLU margins, inclusive equality with zero surplus, conservative open bands, evidence and polarity overrides, dual-use normalization, active-mask routing, fallback behavior, ties, and why zero ReLU output alone does not quarantine a path. |
| [`verification/test_representation_theorems.py`](verification/test_representation_theorems.py) | Encoding factorization, robust decoding, exact ReLU constructions, hard seams, fixed versus expandable libraries, evaluated versus global nondomination, dual-use payload/grade channels, boundary state, normalization, and CPWL plan computation. |
| [`verification/test_policy_value_reconstruction.py`](verification/test_policy_value_reconstruction.py) | Canonical encoder-image identities, the tight `2 rho` tie/flip boundary, event-mass certificates, conservative `4 rho` non-abstention, `Q/V` variants, stochastic modal collapse, hidden lookup, off-support disagreement, state aliasing, IID certification, and trajectory coupling. |
| [`verification/test_losses.py`](verification/test_losses.py) | Width/miss penalties, masking missing targets, schema balance, unit changes, held-out calibration, polarity-aware decoding, symbolic public outcomes, cross-entropy baselines, selective routing metrics, surplus gating, and disjoint data roles. |
| [`verification/test_proof_plans.py`](verification/test_proof_plans.py) | Plain and certificate-carrying execution agree on payloads; errors and resources propagate correctly; missing/self-asserted evidence and cycles are rejected; provenance is grounded; and ranked self-assessment is deterministic. |
| [`verification/test_experiment_protocol.py`](verification/test_experiment_protocol.py) | Synthetic formulas, quotas, exact oracle states, reproducibility, the scientific-succession fixture, updates, scorer-data firewall, proposal binding, role disjointness, metric/power rules, frozen hashes, and the final-world embargo. |
| [`verification/test_experiment_implementation.py`](verification/test_experiment_implementation.py) | The learner cannot import the oracle; features are closed; network capacity/initialization are matched; calibration is independent; boundary, missing, invalid, and polarity cases are exact; masks and traces are safe; the system witness is evidence-bound; and the original entry point is guarded. |
| [`verification/test_experiment_repair.py`](verification/test_experiment_repair.py) | The fast array adapters match the original object path, NumPy matches C++, repaired evaluation matches v1, contract hashes remain current, and preparation/final stages require different tokens. |
| [`verification/test_experiment_analysis.py`](verification/test_experiment_analysis.py) | The paired world bootstrap is deterministic, paired endpoints stay paired, one-sided and Holm calculations behave as intended, wholly missing secondary rows remain explicitly missing, and the committed Task 21 analysis/figures retain their frozen dispositions and safety result. |
| [`verification/test_links.py`](verification/test_links.py) | The whole repository's local Markdown links resolve and deliberately broken sample links are detected. |

## The experiment code

The experiment compares two matched ReLU multilayer perceptrons on artificial, exactly known cases. Artificial data is useful here because the program can know the correct logical state without leaking that answer to the learner. The experiment is preregistered in [`experiments/01_design.md`](experiments/01_design.md); the following files implement that design.

### Scientific core

| File | What it does | Why it is needed |
|---|---|---|
| [`experiments/__init__.py`](experiments/__init__.py) | Marks the experiment directory as a package and states that learner and final-confirmation work belong to later project stages than the generator. | Keeps imports stable and records the trust-boundary intent at package level. |
| [`experiments/protocol.py`](experiments/protocol.py) | Defines experimental roles, schemas, plans, context cells, atom strata, evidence modes, world/request records, deterministic random identities, latent loss/latency laws, exact oracle decoding, active sets, fallback selection, world generation, update fixtures, scorer-input auditing, proposal binding, role manifests, fidelity metrics, and power helpers. | This is the experiment's rulebook and artificial world generator. It separates what the learner may see from the hidden values used only for evaluation and prevents final worlds from being generated without authorization. |
| [`experiments/learner.py`](experiments/learner.py) | Defines the PyTorch ReLU MLP, matched parameter budgets for the structured and cross-entropy arms, paired initialization, structured and classification losses, deterministic batching/training, validation, shared capacity selection, prediction, and model serialization helpers. | The comparison would be unfair if one arm received a larger network, different initial trunk, different data order, or a separate capacity choice. This module centralizes those controls and does not import the generator/oracle. |
| [`experiments/implementation.py`](experiments/implementation.py) | Converts permitted world fields into the fixed 25-number feature vector; makes training panels; calibrates structured intervals; binds proposals to scorer/calibration identities; decodes structured and cross-entropy outputs; derives request outcomes; applies exact masks and fallbacks; constructs boundary/transfer cases; freezes prediction traces before joining hidden evaluation fields; and runs implementation preflight witnesses. | It is the original readable bridge from the frozen protocol to the networks and exact value-logic decisions. It is also the reference against which the faster evaluator is checked. |
| [`experiments/system_witness.py`](experiments/system_witness.py) | Demonstrates how a learned grade proposal becomes usable only after an independent lower-ranked audit binds it to the exact model/calibration. It then builds and verifies a proof-carrying plan while keeping final confirmation lineage separate. | A network's confidence is not self-validating evidence. This deterministic example shows the intended boundary between proposal, external check, composite certificate, and later confirmation. |

### Original runners and pilot

| File | What it does | When to use it |
|---|---|---|
| [`experiments/run_pilot.py`](experiments/run_pilot.py) | Runs the Task 19A **generator-only** pilot on 256 pilot worlds, checks exact panel quotas and invariants, calculates conservative design/power quantities, and writes the frozen pilot, protocol, and role-manifest JSON files. It never fits a learner or materializes production outcomes. | Use for provenance or regenerating the original preregistration artifacts after an explicitly reviewed protocol-version change. It is not the neural experiment. |
| [`experiments/run_experiment.py`](experiments/run_experiment.py) | Implements the original v1 neural preflight, pilot-role smoke test, capacity search, fitting, per-world evaluation, trace writing, and guarded all-at-once final run. | Use `--preflight` or `--smoke` only for historical/reference checks. The all-at-once final path is retained for provenance and differential testing; use the repaired runner for operational Task 21 stages. |
| [`experiments/artifact_io.py`](experiments/artifact_io.py) | Writes sorted, indented UTF-8 JSON with explicit LF bytes and an optional atomic rename. | New experiment versions use it to avoid platform-dependent newline hashes. Historical v1/v1.1 writers are source-hashed evidence and remain unchanged. |

### Repaired block-oriented path

| File | What it does | Why it is needed |
|---|---|---|
| [`experiments/repaired_evaluator.py`](experiments/repaired_evaluator.py) | Packs many worlds into ordinary NumPy arrays, writes the same 25 features directly, prepares probes/boundaries/transfers/requests once per block, predicts in batches, calls the C++ decoder, computes metrics, and reconstructs the registered trace fields. It includes assertions comparing fast and original paths. | The original per-row custom-object path was too slow and triggered interpreter failures at full scale. Blocks preserve the scientific calculation while greatly reducing Python-object churn. |
| [`experiments/cpp_kernel.py`](experiments/cpp_kernel.py) | Defines and validates the numeric input/output array contract, provides a readable NumPy decoder, loads the compiled C++ library with `ctypes`, and demands NumPy/C++ equivalence. | It is the safety adapter between Python and C++. Callers cannot silently pass arrays with the wrong shape, type, or memory layout. The NumPy version supplies an independent readable reference. |
| [`experiments/build_cpp_kernel.py`](experiments/build_cpp_kernel.py) | Hashes the native sources, configures CMake, builds the shared library, runs CTest, locates the platform-specific library, caches a build record, and optionally repeats the test in Debug mode. | Native builds differ by operating system and compiler. This script gives Python one reproducible way to obtain and verify the decoder without committing machine-specific binaries. |
| [`experiments/run_repaired_experiment.py`](experiments/run_repaired_experiment.py) | Verifies the v1.1 contract; runs preflight and pilot checks; and provides atomic, resumable selection, fit, calibration, and confirmation stages. Confirmation is saved in 100-world blocks with hashes for metrics and all trace shards. | It is the current operational entry point. Staging limits the damage from interruption, verifies prerequisites before continuing, and keeps preparation authorization separate from final-confirmation authorization. |
| [`experiments/analyze_results.py`](experiments/analyze_results.py) | Reads the immutable completed v1.1 result and verified trace shards; averages the eight paired fits within each world; performs the registered world bootstrap, one-sided tests, and Holm corrections; summarizes robustness and ablations; and renders three figures. It never regenerates final worlds. | A raw metric file is not a conclusion. This module makes the inferential unit, multiplicity, null margins, claim rules, deviations, and unavailable secondaries explicit and reproducible without reopening the final experiment. |

For more detail about why this path was introduced, see [`experiments/03_execution_repair.md`](experiments/03_execution_repair.md).

## The C++ decoder

The native component is intentionally tiny. It receives arrays already owned and checked by Python, loops over their rows, and writes arrays back. It does not generate worlds, load files, allocate model objects, train a network, or decide which experiment to run.

| File | Plain-language purpose |
|---|---|
| [`experiments/cpp/value_logic_kernel.h`](experiments/cpp/value_logic_kernel.h) | Declares the one C-compatible function `vl_decode_block_v1`. The stable C interface is what Python's `ctypes` loader can call on Windows, Linux, or macOS. |
| [`experiments/cpp/value_logic_kernel.cpp`](experiments/cpp/value_logic_kernel.cpp) | Implements interval decoding, three-class argmax/confidence, evidence/binding/polarity overrides, and signed/ReLU margins for every row. It returns numbered error codes for invalid pointers, row counts, or schema values. |
| [`experiments/cpp/value_logic_kernel_self_test.cpp`](experiments/cpp/value_logic_kernel_self_test.cpp) | Runs one critical equality-boundary case—`Supported` with zero strict surplus—and confirms that an invalid schema is rejected. | 
| [`experiments/cpp/CMakeLists.txt`](experiments/cpp/CMakeLists.txt) | Tells CMake to compile a C++17 shared library with strong warnings, build the self-test, link it to the library, and register it with CTest. |

The decoder emits five state views because the registered study includes the full structured arm and several comparisons/ablations:

- calibrated structured state;
- center-only structured state;
- shadow or variant structured state;
- cross-entropy state; and
- self-confidence ablation state.

It also emits signed support/refutation margins and their ReLU-positive parts. These numbers describe one comparison. The later Python code still needs well-formedness, all required atoms, and the exact active mask before it can derive a full license or route.

## How data moves through the neural experiment

1. `protocol.world_identity(role, index)` assigns a deterministic identity without needing to expose its hidden answers.
2. `protocol.generate_world(...)` builds probes and multi-atom requests for that role. Final-confirmation generation is guarded.
3. `implementation.py` or the equivalent fast adapter in `repaired_evaluator.py` projects only whitelisted pre-outcome fields into a 25-number feature vector.
4. `learner.py` trains matched structured and cross-entropy MLPs. The learner has no generator/oracle import.
5. A disjoint calibration role estimates expansions for the structured intervals and binds them to the exact fitted scorer and schema.
6. The C++/NumPy decoder maps each proposal plus accepted evidence metadata to `Refuted`, `Open`, or `Supported`.
7. Request-level logic combines atom states with well-formedness. The exact active mask keeps only licensed plans; the router chooses among them or uses the fallback.
8. Metrics and prediction traces are written. Prediction fields are hashed before hidden oracle/evaluation fields are joined, making leakage easier to detect.

## Experiment artifacts and what they mean

JSON files are human-readable metadata or results. NPZ files are compressed NumPy arrays, used here for PyTorch model parameters. JSONL trace files contain one JSON record per line. Some later-stage artifacts may not exist until their stage completes.

Several frozen JSON contracts use raw-byte SHA-256 hashes. Seven v1/v1.1 artifacts were originally written with CRLF on Windows; [`.gitattributes`](.gitattributes) now preserves their exact registered bytes instead of letting Git normalize them. Other JSON files retain their own existing bytes. Do not run a line-ending converter across the directory. New versions should use `artifact_io.py` or explicitly declare a different canonical serialization before hashing.

| Artifact | Meaning |
|---|---|
| [`experiments/protocol_v1.json`](experiments/protocol_v1.json) | Frozen scientific design, role counts, hypotheses, estimands, thresholds, and embargo rules. |
| [`experiments/manifests_v1.json`](experiments/manifests_v1.json) | Deterministic identities/digests proving that train, calibration, audit, and confirmation roles are lineage-disjoint. It does not contain generated final targets. |
| [`experiments/pilot_results_v1.json`](experiments/pilot_results_v1.json) | Task 19A generator-only pilot summaries and conservative sizing inputs. Not confirmatory evidence. |
| [`experiments/implementation_v1.json`](experiments/implementation_v1.json) | Frozen hashes and configuration for the original v1 implementation. |
| [`experiments/implementation_smoke_v1.json`](experiments/implementation_smoke_v1.json) | Small pilot-role neural smoke-test record. It establishes execution, not a scientific endpoint. |
| [`experiments/implementation_v1_1.json`](experiments/implementation_v1_1.json) | Frozen v1.1 execution-repair contract and source hashes. It states that the execution method changed while the registered scientific design did not. |
| [`experiments/implementation_repair_pilot_v1_1.json`](experiments/implementation_repair_pilot_v1_1.json) | Pilot-role equivalence and performance-gate record for the repaired path. Not final evidence. |
| `experiments/selection_checkpoint_v1_1.json` | Shared network-capacity search and the selected budget. Its presence means selection wrote a checkpoint, not that later stages or hypotheses are complete. |
| `experiments/model_states_v1_1.npz` | Parameters for the eight paired fitted structured/cross-entropy models. This can be large and is ignored by Git. |
| `experiments/fit_checkpoint_v1_1.json` | Model identities, fit summaries, and hashes binding the fit stage to its contract and NPZ file. |
| `experiments/calibration_checkpoint_v1_1.json` | Held-out calibration groups/radii bound to the fitted models and calibration role. |
| `experiments/confirmation_progress_v1_1/` | Per-block metrics and completion markers used to resume confirmation safely. A marker is trusted only after its hashes verify. |
| `experiments/trace_shards_v1_1/` | Detailed per-seed prediction/evaluation traces, divided into restartable world blocks. |
| `experiments/raw_results_v1_1.json` | Complete raw registered metrics assembled only after every confirmation block verifies. It is the input to analysis, not automatically the paper's conclusion. |
| [`experiments/analysis_v1_1.json`](experiments/analysis_v1_1.json) | Compact machine-readable Task 21 estimates, uncertainty, `F35/F36` rule outcomes, seed sensitivity, secondary summaries, safety checks, deviations, and claims not made. It binds back to the raw result and every stage checkpoint by SHA-256. |
| [`experiments/02_results.md`](experiments/02_results.md) | Reader-facing explanation of the completed result: strong structured tolerance transfer, weak boundary/in-regime performance, supported narrow marginal coverage, ablations, limitations, and project impact. |
| [`experiments/figures/`](experiments/figures/) | The three committed plots rendered from `analysis_v1_1.json`: primary endpoints, marginal coverage, and ablations. |
| `experiments/model_states_v1.npz`, `trace_shards_v1/`, or `raw_results_v1.json` | Original v1-path artifacts. They are not interchangeable with v1.1 checkpoints. |
| [`experiments/task21_failure_attempt1.json`](experiments/task21_failure_attempt1.json), [`experiments/task21_failure_attempt1.md`](experiments/task21_failure_attempt1.md), [`experiments/task21_interruption_attempt2.json`](experiments/task21_interruption_attempt2.json), and [`experiments/task21_runtime_diagnosis.md`](experiments/task21_runtime_diagnosis.md) | Provenance records for the failed/interrupted original execution and its diagnosis. They are engineering evidence, not hypothesis results. |

Do not infer stage completion solely from a file name. The repaired runner verifies version, source, prerequisite, and content hashes before reusing a checkpoint.

## Safety boundaries that are easy to miss

- **A learned output is a proposal.** It becomes accepted evidence only after external validity, identity, calibration, expiry, and polarity checks.
- **Positive ReLU is not “licensed.”** A positive named channel can mean predicted slack or certificate-relative surplus for one atom. The public license still needs the whole symbolic decision.
- **Zero ReLU is ambiguous.** It can occur at supported equality or after a negative/open/refuted/missing/invalid case. State/evidence channels disambiguate it.
- **Cross-entropy cannot overrule missing or invalid evidence.** The direct classifier is evaluated under the same exact usability and polarity gates.
- **The learner cannot see the oracle.** Hidden reference values are joined only in the evaluation namespace, after predictions have been frozen and hashed.
- **Roles are not interchangeable.** Pilot, train, validation, calibration, system-audit, and final-confirmation worlds have distinct identities and purposes.
- **Final confirmation is special.** Preflight, unit tests, the deterministic system witness, and repair pilots do not cross the final embargo. The explicit final token and an authorized Task 21 step do.
- **Hash errors should be investigated.** Do not edit a contract hash, delete a checkpoint, or rename an old artifact merely to make a guard pass. An intentional code change needs a reviewed new implementation version and repeated equivalence checks.
- **Line endings can be evidence.** Frozen raw-byte hashes cover the committed bytes, including newlines. Preserve `.gitattributes`; use the LF-stable writer for new versions rather than rewriting historical source-hashed runners or normalizing all JSON together.

## Troubleshooting

### Python cannot import NumPy, Torch, or Matplotlib

Activate the intended virtual environment and install the pinned requirements:

```powershell
.venv\Scripts\Activate.ps1
python -m pip install -r experiments/requirements.txt
```

Use the same `python` for installing and running. `python -m pip --version` shows which interpreter owns the installation.

### CMake or a C++ compiler is missing

Install CMake and a C++17 toolchain, open a new terminal, and run:

```powershell
cmake --version
python -m experiments.build_cpp_kernel --verify-debug
```

On Windows, a normal Visual Studio installation can exist while its C++ workload is absent. Add the workload through Visual Studio Installer.

### The native library is stale

The build script normally compares source hashes. To deliberately discard its native build cache and rebuild:

```powershell
python -m experiments.build_cpp_kernel --force --verify-debug
```

This affects `.cache/`, not scientific results.

### A source-drift or contract-hash check fails

A frozen source or protocol file differs from the version named in its implementation JSON. Preserve the failure message and inspect `git diff`. If the change is intentional, treat it as a new implementation amendment, rerun the relevant tests/differential pilot, and freeze a new contract. Do not simply replace the expected digest.

### A Task 21 run was interrupted

Do not start over by deleting files. Rerun the same repaired stage. It will validate and reuse a complete checkpoint or completed confirmation block. If it reports a partial block or hash mismatch, preserve the files and audit them; the runner refuses to guess.

### Tests are slow

The full verification command includes PyTorch and native repair checks. To isolate the lightweight semantic tests, run one module, for example:

```powershell
python -m unittest verification.test_kernel
```

To isolate experiment layers:

```powershell
python -m unittest verification.test_experiment_protocol
python -m unittest verification.test_experiment_implementation
python -m unittest verification.test_experiment_repair
```

### A local Markdown link fails

Run `python -m verification.check_links .`. The report names the source Markdown file, the broken target, and the reason. Links are resolved relative to the file containing them.

## Where to start if you want to read the code

For the logic, read in this order:

1. [`verification/kernel.py`](verification/kernel.py)
2. [`verification/test_kernel.py`](verification/test_kernel.py)
3. [`verification/witness.py`](verification/witness.py)
4. [`verification/test_witness.py`](verification/test_witness.py)

For the neural experiment, read in this order:

1. [`experiments/01_design.md`](experiments/01_design.md)
2. [`experiments/protocol.py`](experiments/protocol.py)
3. [`experiments/learner.py`](experiments/learner.py)
4. [`experiments/implementation.py`](experiments/implementation.py)
5. [`experiments/repaired_evaluator.py`](experiments/repaired_evaluator.py)
6. [`experiments/cpp_kernel.py`](experiments/cpp_kernel.py) and [`experiments/cpp/value_logic_kernel.cpp`](experiments/cpp/value_logic_kernel.cpp)
7. [`experiments/run_repaired_experiment.py`](experiments/run_repaired_experiment.py)

For the proof-carrying computation idea, pair [`formalism/08c_proof_carrying_plans.md`](formalism/08c_proof_carrying_plans.md) with [`verification/proof_plans.py`](verification/proof_plans.py) and its tests.
