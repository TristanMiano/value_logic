# Repricing bridge: persistent MaxSAT cores and checked tree profiles

Contributor: **ChatGPT (GPT-6 Astra Pro)**. October 12, 2026 UTC.
DEVELOPMENT literature bridge for [weighted repair](maxsat_findings.md) and
[retained action profiles](repair_profiles.md). Two primary methods were read;
this is a constructive baseline selection, not a novelty or performance audit.

## Directly relevant primary methods

**[1] Andreas Niskanen, Jeremias Berg and Matti Järvisalo (CP 2021),
[Enabling Incrementality in the Implicit Hitting Set Approach to MaxSAT Under Changing Weights](https://doi.org/10.4230/LIPIcs.CP.2021.44).**
Read Sections 3–4.3, especially Algorithm 2 and the weight-update procedure,
pp. 44:4–44:11. The method retains weight-independent cores, changes the
hitting-set objective, and reprices the prior feasible model. Subsequent
weights may depend on previous solutions. Weight-based hardening and reduced
cost fixing require special treatment; permanently retaining their old
consequences is unsound. This is a close existing comparison for our task.

**[2] The same authors (SAT 2022),
[Incremental Maximum Satisfiability](https://doi.org/10.4230/LIPIcs.SAT.2022.14).**
Read Sections 3–5.3, particularly the IPAMIR API and conditional-core method,
pp. 14:4–14:12. iMaxHS implements the broader interface. Conditional cores
retain assumption dependencies; current assumptions determine which
restrictions can enter optimization. The interface distinguishes a feasible
incumbent from a proved optimum. Figure 1 supplies no independent certificate
export function; a solver status is not our checked-proof receipt.

| Update | CP 2021 method studied | SAT 2022 interface |
|---|---|---|
| Change existing soft weights | Yes; includes nonnegative updates | Yes; overwrite a declared soft literal's weight |
| Add hard or soft clauses | Outside its weight-only formulation | Yes |
| Change user assumptions | Outside its formulation | Yes; conditional cores |
| Remove constraints | Not this formulation | Zero soft weight; guarded hard clauses with assumptions |

These are claims about the cited methods and interface, not a survey of every
solver available today. The strongest directly matching baseline identified
here is **persistent iMaxHS/IHS with objective updates**, with all supported
internal reuse enabled. Rebuilding an optimizer for each weight vector is a
useful cold control but does not measure the full existing reuse opportunity.

## A practical comparison interface

Use one persistent optimization object with stable original clause IDs and
stable relaxation literals. Encode soft C_i with hard C_i OR r_i and objective
term w_i r_i. Under the convention in [2], `ipamir_add_soft_lit(r_i,w_i)`
declares that cost term; repeating it changes the weight. Use
`ipamir_add_hard`, `ipamir_assume`, `ipamir_solve`, `ipamir_val_obj` and
`ipamir_val_lit` for the other operations. The paper's weights use unsigned
64-bit integers. Any rational scaling needs exact, checked conversion.

For our own checked service, the useful outer contract is:

```text
reprice(source_id, hard_ids, soft_ids, new_nonnegative_weights,
        retained_tree_ids, retained_witness_ids, budget)
  -> (lower_bound, feasible_upper_bound, chosen_witness,
      checked / unresolved status, proof_dependencies, full_invoice)
```

The source and weight vectors have separate identities. Repricing preserves
the hard/soft meanings; it recomputes every numeric bound. A caller may then
ask for a tolerance on the repair-or-replace action instead of exact optimality.
All ordinary controls receive identical tree and witness reuse, current
objective evaluation, and output precision. Report update/checking time,
new proof acquisition, search time and retained state separately. The
production comparison remains a follow-up; no solver was installed or run
for this note.

## Constructive combination with our retained profiles

The following is a derived interface proposal, not an experimental result
reported by either paper.

Our current checked tree gives a lower bound L_tree(w), while checked witness
violation vectors give U(w). Suppose a separately acquired checked core bank
supplies globally valid constraints on violation indicators z:

```text
sum_(i in K) z_i >= 1, for every checked core K.
L_core(w) = min { w dot z : z is Boolean and satisfies those constraints }.
```

Every feasible repair induces such a z, so `L_core(w) <= C*(w)`.
Consequently `max(L_tree(w),L_core(w)) <= C*(w) <= U(w)` combines the two
receipts immediately. Computing and certifying L_core is paid work; retained
cores do not provide its new numeric optimum for free. A previous negative
budget tree also does not automatically supply globally valid UNSAT cores.

A more integrated option uses each non-hard-conflict leaf's forced-violation
vector p_l. Solve the core-cover problem additionally constrained by
`z >= p_l`, then minimize those optima over leaves. Every feasible assignment
is covered by a leaf and its violation vector satisfies both restrictions.
This proves a valid lower bound at least as large as either separate bound.
It could tighten incomplete trees without reconstructing the full original
search, but there may be many leaves and each auxiliary optimization is
charged. No cost advantage has been measured.

For changed nonnegative weights, the immediate useful distinction is between
reusable structural evidence and old numeric conclusions. Structural branch
coverage, forced violations, checked cores and feasible witnesses can support
new prices. A scalar old optimum or an objective-dependent pruning decision
needs its dependencies reconstructed before reuse. The current source-bound
profile work makes that dependency explicit and provides a compact interface
for later comparison with the stronger persistent baseline.
