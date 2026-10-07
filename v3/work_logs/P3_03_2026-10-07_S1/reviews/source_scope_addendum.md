# P3-03 — Source-scope addendum for principal §§6–9

Reviewer: **ChatGPT (GPT-6 Astra Pro)**, `/root/bounded_sources`.
Same-model internal, nonblind review. Observed UTC:
**2026-10-07T15:19:20.059224+00:00**.

Reviewed [principal draft](../../../derivations/03_logical_uncertainty.md)
SHA-256 `c82f9764a51a80adccf942f7fc44b28455ec7340048b09ae0c92997e33b951d3`.
The UTF-8 text from the `## 6.` heading through immediately before `## 10.`
has SHA-256 `7fe0b91ce67036272e93e2f274378049bd870a2ef39c4f89c41e7998df247fe3`.
Sections 1–2 were also inspected only to establish the declared source and
semantic-coverage assumptions.

## Finding

**The draft stays within the inspected primary-source hypotheses.** Its
results are presented as a restricted finite construction and elementary
arguments; they do not acquire stronger learning or runtime guarantees by
citing the ordinary sources. One completion qualifier below should be carried
into the final §9 statement.

| Principal section | Assessment against the [source contracts](../../../literature/03_bounded_sources.md) |
|---|---|
| §6 | The distinction between a nonempty outer cover, a witnessed feasible source and a fully coherent probability adapter is explicit. The extrema identity has a nonempty finite source and is proved by convex combinations and point masses. It supplies no selected prior or efficient optimizer. |
| §7 | The bounded execution question has its own horizon semantics; a spent reasoning budget is separately unresolved. A checked signed answer is distinguished from a generic negative algorithmic-knowledge response. Replaying a receipt is not described as an independent interpreter or a proof of the host implementation. |
| §7.1–7.2 | Per-transaction work has explicit finite caps and separate cost categories. Atomic cover publication and direct signed-coordinate uptake address the intermediate-state boundary. The source audit does not substitute for checking that the implementation actually enforces these conditions. |
| §8 | Reset after withdrawal is a conservative project policy with explicit lost-work costs. The draft claims neither an optimal ATMS repair nor free reconstruction. Changed query identities and objective versions remain separate. |
| §9 | Fixed-query resolution explicitly requires finite admissible computation, scheduling, retained progress and retained results. The growing-query example refutes a careless quantifier inference without claiming a universal lower bound. No Logical Induction guarantee is imported. |

## One requested clarification: finite completion under all resource caps

The reviewed §9 finite-fragment paragraph conditions exact completion on fair
splitting/checking and sufficient frontier storage. Section 7.1 also permits
arithmetic or other resource limits. The final completion claim should therefore
require that **all necessary checks and loss-report operations fit their
declared caps and are eventually scheduled**, in addition to sufficient
frontier storage. Otherwise a typed resource limit can be the sound result
even after enough abstract refinement opportunities have elapsed.

It should also distinguish **exact extrema for nonempty $F(H)$** from a
**finite-conflict result when $F(H)$ is empty**. Section 6 already does so;
the same qualification belongs in the conclusion of §9. This is a local
consistency clarification, not a challenge to a cited theorem.

The binary-tree node count is a structural bound on distinct processed nodes
for the stated complete refinement. It is not by itself a bound on host CPU
cost, repeated scheduling or arbitrary formula evaluation. The draft's
separate operation accounting is therefore material to any eventual resource
claim.

## Scope and preservation

This addendum reviews the named draft only. It does not certify later code,
development results, task completion or contribution support. No principal
edits, experiments, clock changes, status changes or publication actions were
performed. There is no additional concurrent time credit.
