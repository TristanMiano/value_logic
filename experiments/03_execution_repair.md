# Using the repaired Python/C++ experiment runner

## The short version

The original experiment code asked Python to create, inspect, and repeatedly audit millions of small custom objects. That is easy to read one object at a time, but it became both very slow and unreliable at the full experimental scale. One run ended inside the Python interpreter after about 35 minutes; a second was stopped after the project's total run time passed an hour.

The repaired implementation keeps the experiment itself the same. It changes how the already-defined calculation is carried out:

1. Python creates each synthetic world once and packs its relevant numbers into rectangular NumPy arrays.
2. PyTorch trains the same ReLU networks and predicts a whole block of rows at once.
3. A small C++ function turns those numeric predictions into exact logical states for the whole block.
4. Python computes the same registered metrics and saves a checkpoint after every completed stage or world block.

An everyday analogy is replacing thousands of individually addressed envelopes with one labeled tray. The information and destination do not change; moving the tray is faster and involves fewer things that can go wrong.

Task 20R ran only the repair checks and a pilot. It did **not** generate or inspect the final data and did not decide whether the scientific hypotheses are true.

## Why both languages are used

Python remains the main language because NumPy, PyTorch, experiment configuration, and JSON/NPZ checkpoint handling are mature and readable there. Most of the project is still Python.

C++ is used only for the compact semantic hot path: given model outputs and already-checked metadata, decide whether each atom is `Refuted`, `Open`, or `Supported`, and calculate its signed and rectified margins. This loop is simple arithmetic over caller-owned arrays. It creates no Python objects, calls no Python callbacks, allocates no hidden per-row memory, and does not train a network.

The C++ is necessary here for engineering reliability, not for mathematical authority. A C++ answer is not automatically correct. The project therefore keeps a readable NumPy implementation of the same function and requires exact agreement on 10,000 randomized rows. It also compiles and runs a native self-test in both optimized Release and unoptimized Debug modes.

## What the decoder actually does

For a structured prediction, the network proposes a center and a nonnegative radius. Accepted held-out calibration adds a separately computed expansion. The decoder compares the resulting interval with the atom's threshold:

- the upper endpoint at or below the threshold can support an upper-bound atom;
- the lower endpoint strictly above the threshold can refute it;
- an interval crossing the threshold is open;
- missing, invalid, wrongly bound, or polarity-incompatible evidence is open.

The decoder also handles the direct three-class cross-entropy prediction, but exact evidence and polarity checks can override that prediction to `Open`. Its margin outputs do not grant a full license. A positive support margin is strict surplus for that one decoded comparison; equality is supported with zero surplus. A full license still requires all atoms in the profile, well-formedness, and exact active masking.

## What each file is for

| File | Plain-language purpose |
|---|---|
| `repaired_evaluator.py` | Packs worlds into arrays, performs batched prediction, computes metrics, and constructs the same trace fields as v1. |
| `cpp_kernel.py` | Defines the array contract, contains the readable NumPy reference, loads the compiled library, and compares their answers. |
| `cpp/value_logic_kernel.h` | Declares the single C-compatible block function. |
| `cpp/value_logic_kernel.cpp` | Implements the allocation-free arithmetic decoder. |
| `cpp/value_logic_kernel_self_test.cpp` | Checks a critical boundary case and malformed input without involving Python. |
| `build_cpp_kernel.py` | Uses CMake to build and test the local library under `.cache/`. |
| `run_repaired_experiment.py` | Provides guarded preflight, pilot, selection, fit, calibration, and confirmation commands with atomic checkpoints. |
| `implementation_v1_1.json` | Freezes source and protocol hashes plus the exact meaning of the execution-only amendment. |
| `implementation_repair_pilot_v1_1.json` | Records equivalence and performance-gate evidence from pilot-role data only. |
| `verification/test_experiment_repair.py` | Regressions for feature, calibration, C++/NumPy, old/new evaluator, and authorization equivalence. |

## Requirements and first use

Run commands from the repository root. Install the pinned Python packages in `experiments/requirements.txt`. A C++17 compiler, CMake, and CTest must be available. On Windows, the tested toolchain is Visual Studio 2022 Community with its C++ workload; on Linux or macOS, CMake can use the installed C++17 compiler.

Build and test just the native component:

```text
python -m experiments.build_cpp_kernel --verify-debug
```

This writes only disposable, machine-specific files under `.cache/`. The binary is not committed. Its source and binary hashes are recorded locally.

Run the complete non-production preflight:

```text
python -m experiments.run_repaired_experiment --preflight
```

This verifies all frozen hashes, builds/tests C++, compares NumPy with C++ on 10,000 random rows, compares the fast adapters with the v1 reference, checks the final-data embargo, and runs the deterministic system witness.

Run the bounded repair pilot:

```text
python -m experiments.run_repaired_experiment --pilot
```

The pilot performs a deliberately tiny fit, a complete old-versus-new differential check, and a 100-world timing block. It refuses to pass if projected confirmation evaluation exceeds 900 seconds. It does not use production or final-confirmation worlds.

## The future Task 21 production stages

These commands are documented so a later model or person can resume the project, but they were **not run during Task 20R**. Run them in order only when undertaking Task 21:

```text
python -m experiments.run_repaired_experiment --task21-select PREPARE-VALUE-LOGIC-REPAIR-V1-1
python -m experiments.run_repaired_experiment --task21-fit PREPARE-VALUE-LOGIC-REPAIR-V1-1
python -m experiments.run_repaired_experiment --task21-calibrate PREPARE-VALUE-LOGIC-REPAIR-V1-1
python -m experiments.run_repaired_experiment --task21-confirm RUN-VALUE-LOGIC-REPAIR-FINAL-V1-1
```

The first three use a preparation token. The untouched final-confirmation worlds require a different exact token. This separation makes an accidental final run less likely.

| Completed stage | Main checkpoint |
|---|---|
| Selection | `selection_checkpoint_v1_1.json` |
| Eight paired fits | `fit_checkpoint_v1_1.json` and ignored `model_states_v1_1.npz` |
| Held-out calibration | `calibration_checkpoint_v1_1.json` |
| Confirmation block | ignored metrics/marker files under `confirmation_progress_v1_1/` and traces under `trace_shards_v1_1/` |
| All confirmation blocks | `raw_results_v1_1.json` |

Every stage writes its file atomically: it first completes a temporary file and then renames it. Confirmation works in 100-world blocks. On restart, a completed block is reused only after the saved metrics hash and all eight trace-shard hashes verify. A lone marker or metrics file is treated as a partial block and requires an audit rather than being silently trusted.

## What was proved equivalent, and what was not

The repair tests establish the following implementation facts on pilot-role cases:

- training and evaluation feature arrays match v1 bit for bit;
- full and center-only calibration match v1 while sharing one prediction pass;
- logical states, outcomes, masks, routes, and integer trace fields match exactly;
- the NumPy and C++ decoder outputs match bit for bit;
- complete world metrics match to an absolute scalar tolerance of `2e-12`;
- float trace values use an absolute tolerance of `1e-5` because batched and single-world float32 matrix multiplication can differ by a few last-place bits. The largest pre-freeze randomized-pilot difference was about `7.63e-6` after conversion to latency units.

The last tolerance does not permit a logical answer to change. Discrete states and decisions must still be identical. If a small numeric difference crosses a decision boundary, the differential test fails.

These tests do not prove the experiment's hypotheses, general C++ correctness, or scientific validity beyond the frozen synthetic design. They show that the new execution path is a faithful and much smaller reliability surface for running that design.

## Troubleshooting

- **“CMake is required”:** install CMake and a C++17 toolchain, then open a new terminal so `cmake` and `ctest` are on `PATH`.
- **“source drift”:** one of the frozen v1.1 source files changed. Do not edit the JSON hash to make the error disappear. Review the change, give it a new implementation version if intentional, rerun all differential checks, and freeze a new contract.
- **“pilot is stale”:** the pilot record belongs to a different contract or failed its performance gate. Rerun `--pilot` after verifying why the contract changed.
- **checkpoint hash mismatch:** preserve the files and audit them. Do not delete or overwrite evidence merely to continue.
- **partial repaired block marker:** inspect the named progress and trace files. The runner intentionally refuses to guess whether an interrupted write is valid.
- **old `model_states_v1.npz` or `trace_shards_v1/` files:** these belong to the failed/interrupted v1 attempts. The v1.1 runner never treats them as repaired checkpoints.

For the failure history and measured old bottleneck, see `task21_runtime_diagnosis.md`. For the unchanged scientific implementation, see `02_implementation.md` and `01_design.md`.
