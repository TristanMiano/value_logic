# P3-A-1: hostile review of the restricted representation

Contributor: **ChatGPT (GPT-6 Astra Pro)**, delegated reviewer
`/root/retention_bridge`, October 7, 2026 UTC. Same-model internal, nonblind
review. **Zero additional principal time credit.** Only this review file is
written; no scientific probe, clock, ledger, source, control or algorithm is
changed or executed.

**Finding:** the drafted finite constraint/expected-loss/certificate interface
satisfies the **usable restricted representation** prerequisite at the scope
stated in the reviewed gate draft. It has explicit finite inputs, nonvacuous
outputs, constructive obstructions and exercised checking interfaces. It does
not need a complete-model, truth or calibration oracle to establish those
conditional mathematical services. No substantive representation blocker was
identified under that scope. This is a scoped recommendation to the principal,
not the final gate verdict or a finding that a logical learner exists.

## 1. Reviewed snapshots and provenance

The gate baseline names published main
`fb9623f4c725eb25ea8e13dccbd5704d61b4481a` and source tree
`c9b3bc7eb92af9dffc32db9e817f1917e5f6a952`. The gate log explicitly explains
that local Git HEAD remains the older `ad1b0d15114ae0fbd48f671cdd58494bf3b3149c`
while the saved index matches the published source tree. This review identifies
actual bytes rather than treating local HEAD as the published version. Every
protected P3 source/evidence item hashed below matched its entry in the gate
baseline. The live TODO and gate draft are current assessment inputs, not
historical completion artifacts.

| Read artifact or input | SHA-256 snapshot |
|---|---|
| `TODO_v3.md`, P3-A criterion and P3-03 ownership | `060b7c839818d0401c43ba88a2d051db1888da7f88a637f031b326c7f1f090f6` |
| `v3/checkpoints/A_1.md`, assessment-in-progress draft, §§1–6 | `dc09e27cd9c01929e93aaf25d214b028d9fe353fc0969836d234188f46838127` |
| `v3/work_logs/P3_A_2026-10-07_S1/baseline.json`, source/preservation fields | `d32bd21f652c30ef9f993690183b2fa065041bcd70bf2f2bbf7539caa8a42e03` |
| `v3/RESEARCH_PROTOCOL.md`, gate versus task obligations | `ef57593ce23cbe06b1683fc3609526f700b6ab5c395befacbbcd01bd48f3aa52` |
| `v3/foundations/01_problem_contract.md`, §§2–5 | `2c32e1a8cc454f92e16f647df9c0d50d2db008e0dd6d2d1e99a90d11d42d2de7` |
| `v3/foundations/01_desiderata.md`, U01–U04, V01/V02/V04, R01/I01 | `0c1b250e1e22640c1a965015e009ed18a2661415af83f5086b893f0182376774` |
| `v3/foundations/01_representation_boundaries.md`, §§1–2 | `2b8cc22c9f4f33cfd254936ffa91f63a7102736ee1df1cc073ba6b552f02a6d8` |
| `v3/foundations/01_observation_contract.md`, §§1–6 | `7199b8c591bbe2543914fa5ad822aaaff3167b5651c3c6e936b38adcdd1d906b` |
| `v3/derivations/02_probability_information.md`, especially §§2–6, 13, 19, 21 | `282347f8ee93cc73e982c5d48f4e6731bbbfc962601908f5ba15e2435977b2d2` |
| `v3/checks/02_finite_information_audit.py`, request and certificate interface | `546a4b12df2348d284582de7e48e19378bd8a5fbc3ea191b9190605aaa9879b0` |
| `v3/checks/02_finite_information_verify.py`, arithmetic acceptance boundary | `9b1e2822a867f934fbbaa4b6b7fb1230ad69cbf9458565da1b3bf418e7d3f1f1` |
| `v3/checks/02_native_probability_check.py`, supplied contexts/receipts | `dcfc32c51000ff7b3ed4ff95fd309bdb360dd8f78f25e1c048ddc8e1ee56236a` |
| `v2/derivations/02_inference_rules.md`, §§1–5 and preserved operational limits | `fdade0a7650d50280c7d878c5e28d1cca72471165be05ee79e25284deb708e28` |

The saved native result
`v3/work_logs/P3_02_2026-10-07_S1/development/native_probability_agent.json`
has SHA-256
`efd37c659e89467a6f71554ef1c315d42010bdd16185b6f3d338a46a0366d426`.
Its metadata and relevant supplied context/receipt construction were inspected;
the million-byte trace was not freshly reverified here. It records five supplied
groups, 13 accepted targets, three expected rejections and the reduct
countermodel.

The corresponding standalone interface records are:

| File under `v3/work_logs/P3_02_2026-10-07_S1/development/` | SHA-256 |
|---|---|
| `constructive_cli_2.json` | `2ad01a27047693ac9a84ec4a916ed78efdc392d933936f02d43f05d6ffb6a8ce` |
| `constructive_cli_2_files/input.json` | `ffdc714a103b991ff741c4d7e4e2979e1d6c6d37338f7db1ecfb17fe4a7cb2e7` |
| `constructive_cli_2_files/certificate.json` | `159ce94a45b1a39a8fc7c13ef7385c60e78daf10702435888b59adc24420ca05` |

The earlier detailed provenance review remains
[constructive_evidence_scope.md](../../P3_02_2026-10-07_S1/reviews/constructive_evidence_scope.md).
Existing evidence retains its original DEVELOPMENT status; reuse here adds no
run, independent replication or historical time. Later revisions of the live
gate draft need their own principal reconciliation.

## 2. What is actually usable now

“Finite rational source” should mean a **finite rational description**, not
necessarily a finite set of laws or a claim that every law has rational
coordinates. A rational polyhedron can describe real probability vectors.
The smallest supported case is a named finite assessment space, normalization,
known rational payoff rows and a specified target. These labels can be supplied
mathematical scenarios. They need not be complete models of arithmetic.

Two existing interfaces supply concrete, distinct services:

1. **Design-level certificate service.** The companion accepts rational `L,C`
   and one of four exact common scale/offset contracts on the full simplex.
   It returns exact row-identity decoders, actual same-record law/nuisance
   collisions, and free-query repair certificates. This calculation does not
   need a particular unknown law or an oracle for arithmetic truth. The saved
   example uses old row `(0,1,0)` and target `p1`: two added rows recover that
   target while the whole law and offset remain unidentified. Actual values
   still require their expectation/calibration interpretation and access.
2. **Conditional native receipt service.** The inherited checker accepts
   supplied rational source rows, explicit nonemptiness witnesses, legal
   conversion paths and proof traces bound to literal requests. The existing
   fixtures recover a three-state law after proper unit transport and reject
   a negative inequality multiplier and an undeclared probability-unit
   rewrite. The proof rule checks supplied premises; it does not discover
   their truth or promise general proof search.

This is enough for a restricted representation prerequisite: the interface
has a concrete admitted input and a reproducible conditional computation, not
just a list of aspirations. It is less than a complete source manager,
budgeted learner or acquisition policy. The reviewed gate draft §3 states
that distinction explicitly.

## 3. Objections and dispositions

| ID | Hostile objection | Disposition at the reviewed scope |
|---|---|---|
| GA-OBJ-01 | A finite state table hides free access to every complete mathematical model or all consequences of a theory. | **No present blocker.** P3-01 §5.1 expressly denies `models(Gamma)` and free closure; the candidate uses supplied finite assessment cases. Giving a logical interpretation to those cases and generating/refining them under budget is P3-03 work. A candidate that instead requires complete-model enumeration would fail the gate's stated representation contract. |
| GA-OBJ-02 | A feasible normalized source proves its own truth or adequacy. | **Rejected inference, boundary retained.** Nonemptiness and arithmetic consistency are conditional mathematical facts. They do not prove that the source contains an interpreted answer or deployment law. P3-02 §§2/13/21 and gate §3.1 preserve semantic provenance and applicability separately. |
| GA-OBJ-03 | A learned estimate or a realized sample can be inserted as an exact expectation row without further evidence. | **Rejected inference, no gate repair needed.** V01 and the gate observation fields distinguish exact expectations, estimates, realized observations and bounds. No error/calibration theorem is supplied by the record shape. P3-03/06 must justify any later producer or keep its outputs explicitly fallible. |
| GA-OBJ-04 | Recovery algebra licenses an inverse unit path, arbitrary ratio or uncertain product natively. | **Discharged by a concrete obstruction.** With only `P -> U`, loss-unit bounds do not yield the missing probability-unit conclusion; the saved reduct witness and expected rejection demonstrate it. Reciprocal calibration must be declared. Variable ratios stay external; fixed thresholds need a justified positive denominator. Known coefficients and uncertain products remain distinct. |
| GA-OBJ-05 | The mathematical companion implements every rational source, decision-only service, interval or native rule discussed in the note. | **Rejected inference, draft already narrower.** Its implemented domain is the full-simplex exact linear-target service under four calibrations. Native fixtures are a different checked interface. The outer version/status/resource record is a contract, not a new implemented manager. A broader implementation claim would require correction before gate closure. |
| GA-OBJ-06 | Arithmetic verification automatically certifies the caller's actual request and source meaning. | **External binding is mandatory.** `verify(record)` checks the problem inside its artifact. The saved CLI separately compares original bytes and declared fields; native receipts bind independently specified literal targets and context identities. A future caller that omits those checks has not composed the warranted service. The gate explicitly retains the distinction. |
| GA-OBJ-07 | A minimum query count or exact decoder grants free observation, state identification, search, precision, storage or repair purchase. | **Rejected inference, remaining costs explicit.** Free-row repair is a design service, not an acquisition policy. The gate records availability and construction/access/checking costs as inputs or unknowns, never zero by omission. Actual bounded production belongs to P3-03; paid selection/comparison belongs to P3-07/08. |
| GA-OBJ-08 | Failure to solve consistency, find a proof or complete a computation can be reported as false, or an empty source can warrant a favorable cost. | **Contract forbids this; executable update still future.** Supplied nonempty native contexts are checked conditional inputs. U02 and the gate retain pending, failure, conflict and stale statuses. P3-03 must implement those distinctions; P3-A does not claim that the record manager already does so. |
| GA-OBJ-09 | The expected-loss notation is ordinary probability, so technical readiness requires a novelty win. | **Not a P3-A blocker.** The criterion explicitly requires no novelty pass. O-COMB may use the same matrices, certificates and smaller summaries. P3-N01 remains NOT YET SUPPORTED; neither ordinary ancestry nor a gate pass decides whether the narrower adaptation is a useful contribution. |
| GA-OBJ-10 | Passing old fixtures proves a general learner or provides an independent final challenge. | **Rejected inference.** The evidence is development, with scoped same-model reviews, a preserved CLI harness failure and corrected completion. No science was rerun here, and neither a new learning duty nor confirmatory result follows. |

Two operational cautions are particularly important at the handoff. First,
native fixtures include explicit feasibility witnesses and endpoint values.
Those are legitimate **supplied development inputs** for checking the stated
mathematics. They are not evidence that hidden arithmetic labels can be handed
to a bounded learner for free. A future evaluation must account for their
construction and restrict access when they reveal the answer. The gate's
design-level companion example avoids requiring a particular law merely to
prove the design's recovery properties.

Second, an F06/F08 receipt's signed comparison budget bounds a difference of
the modeled expressions in the declared unit. It is **not automatically a VM,
CPU or proof-search budget**. P3-01's reasoner budget and the resource account
remain separate. Reusing a proof can save work only after actual lookup,
matching and checking costs are admitted under the chosen comparison.

## 4. What would actually block this gate

The earliest affected repair is a P3-A candidate-specification correction if
the final gate record omits its admitted source, target service, semantic
status, external/native distinction or cost/access premise. It would also
block if the sole offered instance depended on an unprovided complete-model or
truth oracle, or if its claimed certificate contradicted the actual checker.
A newly discovered false P3-02 load-bearing theorem or broken native bridge
would instead reopen that P3-02 dependency and mark dependent claims stale.
None was identified in this review.

The following absences are **prospective work, not detected gate defects**:
a bounded producer/update algorithm; a useful convergence/calibration theorem;
a model-plurality advantage; justified counterfactual dependencies; and a
budgeted acquisition or paid-resource improvement. Their owners are explicitly
P3-03 through P3-08. Moving them into P3-A would restart later tasks under a
zero-floor gate. Equally, passing this gate cannot waive them.

The reviewed gate draft contains the required restrictions, provisional
choice and meaningful alternatives: direct task losses, full probability or
credal information, proof-status constraints, and source-preserving profiles.
Their switching criteria concern the requested service, available information
and measured cost. They do not imply a mandatory scalar, probabilistic or
neural carrier for all future work.

**Recommendation:** support the restricted-representation criterion at this
conditional scope, retain the explicit P3-03 producer/access obligations and
P3-N01 disposition, and let the principal reconcile the complete gate record.
This review neither executes P3-03 nor grants automatic advancement beyond
the authorized gate.
