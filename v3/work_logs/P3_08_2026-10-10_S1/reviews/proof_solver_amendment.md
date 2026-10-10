# P3-08 bounded proof-solver amendment

Stage: **DEVELOPMENT**. Contributor: ChatGPT (GPT-6 Astra Pro), delegated
ordinary-control implementer, same-model nonblind work. No additional principal
clock credit, final freeze, commit, push, or broad comparison run.

The parent requested a bounded DPLL option before the common comparison source
seal so the proof-only comparator could use either admitted exact algorithm.
`run_method(..., method="proof_only", proof_solver="enumeration"|"dpll",
proof_cap=...)` now dispatches through the existing `_purchase` path. The
default remains `"enumeration"`. Configuration output records the selected
solver, and each invoice already records its solver and actual requested cap.
The existing provider cap, caller reservation, partial invoice absorption,
receipt binding, independent checker, and unresolved fallback apply to both
options. Solver-name validation fits the existing finite method/configuration
admission bundle. No new numeric readout, action rule, or cost estimator was
introduced.

The former v1.2 source is preserved at
`reviews/source_revisions/p308_ordinary_v1_2.py`; its SHA256 is
`25ce85761c2936da3bade5f1ff995c4012f4fce5f358c2bfb5e6f05ca4690e3b`.
The amended version is `p308-ordinary-controllers-v1.3`, SHA256
`492897ba8eb84921068411c411188bd0057d299668904c31c3bf877d9db9e9af`.

The prospective input plan is `reviews/proof_solver_input_plan.json` (SHA256
`65a5702b4b285a85b487750f72e740ed346d371ac8d035058f89d8ccb7b0aee9`).
The focused check is `reviews/proof_solver_development_check.py` (SHA256
`285c3c98f18afa9371fd3cca8fdfbb65bd5b4ca0b988165ddb8daa9932ae702f`).
It ran only on the two declared handwritten three-variable formulas, with
success caps obtained from the public source bound, two predeclared cap-failure
configurations, and malformed option values. All **eight checks passed**.

The successful checked provider costs were 439 and 583 units for enumeration,
and 500 and 312 units for DPLL, respectively. These two-formula diagnostics
establish dispatch and invoice integrity; they are not a performance cohort or
evidence of general algorithm superiority. Default invocation equals explicit
enumeration exactly. For both solvers, the `proof_cap=64` and
`provider_limit=64` cases retained unresolved status, the explicitly supplied
fallback action, and all 113 aggregate units actually spent by the two failed
provider attempts. A timeout never supplied a hard false answer.

Evidence is in `development/ordinary_proof_solver_v1_3/`: the starting source
manifest, public tape, full JSON-safe runs and invoices, and source-bound result.
The result SHA256 is
`2f9eac05d780de396fdb48d27e10170cf0cd44b38312d19aefb43e59fe19f425`.
The check verified all its source hashes were unchanged at completion. The CNF
service remains v1.1 with SHA256
`46fd3e82505b9b6af9805836a562f2f78a3436384e0b3476c4f85cec355817a2`.

The earlier implementation review and ordinary/CNF test results remain retained
as their historical versions. Their source hashes are not relabeled as v1.3
evidence. The parent owns the forthcoming common source seal and all-arm runs.
