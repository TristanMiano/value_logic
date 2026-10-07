# P3-01 composition and contribution boundary

Reviewer: **ChatGPT (GPT-6 Astra Pro), same-model internal sub-agent**.
Date: 2026-10-07 UTC. Nonblind internal reconstruction, not external validation.
Resource time is unmeasured and contributes no principal-clock credit.
Scope: question-contract comparison and contribution criteria. No canonical
edits, experimental design/freeze, P3-02 execution or gate decision was made.
The already reviewed finite-perturbation question was not investigated again.

## 1. Recommendation

Keep **P3-N01 NOT YET SUPPORTED** and make its comparator explicitly include the
controller–forecaster architecture, expected-cost decisions and incremental
certificate bookkeeping. A diagram connecting those components is insufficient
evidence of a distinctive contribution. A useful restricted implementation,
formal adaptation or application may still qualify, provided its actual added
service and comparison scope are identified.

The right question is what the complete system guarantees or makes usefully
available under a declared information, computation and revision contract.
It is not whether the components can be put next to one another. This review
does not establish that a future integration is either novel or unpromising.

## 2. Primary comparison checks

### LI: explicit architectural antecedent

[Logical Induction, arXiv v5, December 7, 2020](https://arxiv.org/html/1609.03543v5),
§7.4, explicitly sketches a resource-limited controller consulting an incompletely
trained inductor and deciding when to train it further; that sketch is marked
speculative. Section 4.8 supplies bounded logically uncertain expectations.
Section 7.4 also identifies unresolved counterpossible and theory-generation
questions. These are different evidential statuses: definition/theorem,
proposed architecture, and open problem.

Exact additional locators inspected: §1.1 Desiderata 15–17; §4.8 Definitions
4.8.1–2, Theorems 4.8.4, 4.8.6 and 4.8.10; §7.4's discussion following
Desideratum 15. The source was reopened directly in this review, rather than
inferred from the local orientation.

### Hay et al.: supplied metareasoning interface

[Hay, Russell, Tolpin and Shimony, Selecting Computations](https://people.eecs.berkeley.edu/~russell/papers/uai12-meta.pdf),
§2, Definitions 1–3, specifies a joint model of action utilities and computation
outcomes, a history state, costly computations and a stopping decision. The
paragraph after Definition 3 permits deadline/budget information in the state.
The conditional outcome law is supplied by the model; this is not a guarantee
that a practical learner can construct that law or cheaply solve the resulting
decision problem. Specialized optimality results were not imported here.

### Incremental checking: supplied bookkeeping antecedent

[Albert, Arenas and Puebla, An Incremental Approach to Abstraction-Carrying Code](https://cliplab.org/papers/inc-acc-lpar06.pdf),
§3.1 defines answer/dependency tables; §3.2 defines incremental certificates and
notes a compression-versus-later-checking issue. Section 4 gives the instrumented
checker. This is an antecedent for retaining dependencies and checking updates,
not a logical-forecasting or learned-computation-value theorem. The paper is
already identified in `paper_v2.md` §11.1.

For expectation-first representations and multiple imperfect models, the current
S13 and S08/S15 cards remain relevant comparisons; see
`v3/literature/01_source_contracts.md` and the linked expectation review.
Their selected assumptions and import limits should remain attached rather
than replaced by a blanket assertion that ordinary methods solve every duty.

## 3. What the ordinary combined comparator may already do

The following is a **constructed comparison contract**, not an assertion that
one cited publication has implemented the entire package.

Give O-COMB the same available queries, evidence, source and program versions,
loss tables, current resource prices, model library, computation catalogue,
repair possibilities and budget as the candidate. It may:

1. Maintain finite probability, expectation or interval forecasts using an
   identified practical algorithm, with a separate hard proof-status record.
2. Convert its forecasts to the same task costs, including known stakes and
   an available fallback.
3. Decide whether to inspect input, run a proof/evaluation procedure, update
   a forecasting method, obtain more evidence, or stop.
4. Record provenance and dependencies; keep alternative useful supports;
   invalidate stale warrants; and recheck or transport surviving material.
5. Maintain several scoped models or predictors and route between them under
   the same objective, rather than being restricted to one allegedly exact model.

If this construction uses the candidate's own successful algorithm, equality is
allowed. An exact reduction can establish that a service is available within
ordinary machinery. It need not make a well-specified application worthless,
but it rules out claiming an exclusive capability of value logic.

The theoretical LI comparison and an executable finite baseline also remain
distinct. The experimental ordinary comparator need not run the entire LIA
construction, and a finite predictor cannot inherit LIA's unrestricted
properties by using the same label. Compare theory with the precise theorem
and finite behavior with matched runnable methods.

## 4. Why individually adequate components do not settle composition

The system must choose what crosses each interface. A forecast is not a
truth receipt; an action-value estimate is not the observation model needed
to value another computation; and a valid old proof is not necessarily a
current task warrant. Those distinctions create concrete obligations.

| Interface | Obligation for a claimed composed service | Failure that would invalidate the stronger claim |
|---|---|---|
| Forecast to decision | Specify the action-loss interpretation, decision rule and sufficient forecast-error assumptions for the reported decision target. | A small average score hides high-stakes mistakes or gives no control of the chosen action's cost. |
| Controller to evidence stream | State which computations can produce which results and how selection affects label delay/coverage. State any fairness/completeness assumptions needed by a learning theorem. | A policy starves claims or selects labels while the analysis assumes the earlier passive or complete stream. |
| Forecast to computation-value model | Specify how beliefs about computation outcomes and future useful information are acquired, and whether they form a compatible conditional model. | A table of true computation benefits is supplied for free, or a changing forecast is treated as one fixed known transition law. |
| Soft forecast to hard warrant | Identify the source, soundness or coverage bridge supporting a claim about actual loss. | The checker proves only an inequality between estimates and the report presents it as a guarantee about deployment. |
| Revision to reused proof | Identify which quantity, program, premise, criterion or observation changed; prove the required transport or mark the receipt stale. | A proof of an old loss expression is relabeled as a proof of the new one without preserving its interpretation. |
| Selected representation to later query | State the permitted future questions, decoding process, available information and reconstruction cost. | The decoder consults discarded data, or accuracy on old queries is treated as sufficient for a new query family. |
| Multi-model state to claimed improvement | Supply equal libraries, information and routing options to the ordinary comparison. | The candidate's apparent advantage consists entirely of being offered an additional useful model. |
| Postprocessing to learning guarantee | Retain the score, comparator, timing and transformation assumptions. | A projection enforces one structural constraint but the report assigns the raw predictor's unrelated regret guarantee to the result. |

A deadline can ensure a bounded number of actions without ensuring good choices.
A consistent finite constraint set can support a correct conditional bound
without establishing good weights. A valid certificate can provide an auditable
reason for an action without improving forecast accuracy. Each resulting claim
needs its own outcome and evidence type.

No universal composition theorem is required by P3-01. The point of the contract
is to identify which restricted interface a later task will actually claim.

## 5. Concrete paired comparisons and ablations

These are possible **question-level diagnostics**, not a frozen arm list. A
later experiment should select those needed by its particular claim; there is
no obligation to implement every row, run a full factorial design or use any
specific distribution, seed, sample count or threshold now.

| Pair or nested comparison | What is held fixed? | What a positive difference would show | Stronger conclusion it would not show alone |
|---|---|---|---|
| Value representation versus ordinary probability/expectation representation | Input evidence, forecast rule, action set, numerical tolerances, update timing and charging. | A representation/implementation consequence at the measured scope, or exact operational equivalence. | A new general uncertainty logic or unique utility representation. |
| Adaptive computation choice versus a fixed schedule; then candidate controller versus equally capable ordinary controller | Forecast information, available computations, paid result interface and task losses. | Whether selection is useful, and whether a further difference survives the strong controller. | That adding a controller is itself new. |
| Learned computation-value model versus stipulated correct model | Computation catalogue and decision objective; model provenance differs explicitly. | Sensitivity to estimating the benefit of thinking; whether an advantage requires oracle information. | A practical learning result from the stipulated-model arm. |
| Candidate dependency reuse versus ordinary dependency reuse; fresh recomputation as a diagnostic | Same source facts, prior artifacts, storage costs, revision and acceptance request. | Whether the particular representation/checking interface changes cost or justified coverage. | Newness of caching or incremental checking in general. |
| Unchanged request versus changed stakes versus withdrawn evidence | Use the same initial evidence and report the changed component explicitly. | Which change causes the claimed interaction or failure and which retained information matters. | A general theory of scientific revision from one priced decision reversal. |
| Single model versus several models; candidate plurality versus ordinary plurality | The second comparison shares the whole library, provenance, routing and acquisition costs. | Whether plurality helps this task and whether the candidate adds anything after matching it. | That fallibility or model coexistence is unique to value logic. |
| Resolved-subset scores versus common issued-cohort assessment | Original forecasts and full exposure history, with later evaluator labels kept separate from agent observations. | Whether apparent success survives the actual selection/coverage contract. | An unbiased full-cohort estimate without the needed labels or sampling assumptions. |
| Static catalogue versus paid catalogue/model construction | The resulting catalogue may be compared, but construction costs and evidence are explicit. | Whether the service depends on having the difficult structural choice supplied. | Autonomous invention of a scientific theory or causal structure from a chosen list. |

For an interaction claim, additionally ask whether removing the proposed
cross-component link destroys the relevant service while preserving information
and other algorithmic opportunities. For example, the issue could be whether
the source-and-query identity accompanying a reused estimate prevents a
particular invalid decision after a change. An ordinary implementation may
enforce that same identity discipline. The useful result would then concern
the explicit interface, guarantee or application, rather than ownership of
the idea of provenance.

Do not require superadditive performance as a definition of integration.
A combined service can be useful because it reliably connects two guarantees
or reduces avoidable reconstruction costs. The comparison must still identify
what changed and why the closest ordinary construction does not already settle
the claimed result.

## 6. Contribution boundary criteria

### Evidence adequate for the present task

P3-01 can establish a coherent question contract, precise antecedents, candidate
objects, assumptions and failure witnesses. That is valuable planning work.
Its completion does not itself support the later scientific contribution.

### A future bounded contribution could take any of these forms

- **Formal adaptation:** a scoped connection between a forecast/evidence rule,
  the available computation policy and a current decision or warrant guarantee,
  with the actual assumptions and cost overhead proved. If the argument is
  an application of an existing theorem, label that type accurately.
- **Specialized application:** an informative family where the exact retained
  information, revised query and permitted repair operations yield a useful
  result or sharp obstruction beyond merely presenting the generic solver.
- **Useful synthesis or implementation:** a concrete interface provides an
  identified service under a realistic bounded information contract, with
  comparisons showing what the organization contributes. It need not beat
  ordinary arithmetic or establish worldwide priority.

The inherited `2 epsilon` decision lemma, elementary payoff inversion, a
generic pipeline diagram or another example of two correlated variables do not
by themselves meet these criteria. They can be supporting pieces of a more
specific contribution.

### A claim record should answer six concrete questions

| Field | Required answer for the eventual P3-N01 record |
|---|---|
| Object | Which exact representation, update/transport rule, bounded service or application family is claimed? |
| Type | Is the result an original theorem, formal adaptation, useful synthesis, implementation or specialized application? |
| Delta | What can be concluded or done that the stated ordinary construction and inspected antecedents do not already directly supply? |
| Magnitude | How broad is the family, how strong is the guarantee, and what improvement/coverage/resource consequence is established? |
| Evidence | Which proof, construction, counterexample or matched result establishes that delta, including adverse and null outcomes? |
| Comparison scope | Which sources and ordinary combinations were checked, and which close comparisons remain incomplete? |

If only a component-level difference remains after the strong comparison, report
it at that level. If an exact translation reproduces the whole service within
the claimed cost allowance, an exclusive-capability claim is defeated; a useful
application claim may still need separate assessment. If a measured gain vanishes
after including model acquisition, source inspection or checking, the original
total-resource advantage is unsupported.

## 7. Suggested canonical clarification and next ownership

Add the explicit §7.4 architectural antecedent to the S01 comparison record and
to the explanation of P3-N01's target. The main contract already keeps support
open and is compatible with this stronger comparison. A suitable target remains:

> Investigate whether a specified cost/uncertainty representation and revision
> interface provides a useful bounded decision or warrant service, with an
> explicit information and resource account, beyond the directly available
> ordinary construction for the same task.

P3-02 can next identify the representation and recovery question. P3-03/06/07
own the actual logical-evidence update and learning/computation guarantees;
P3-04/05 own the selected counterfactual semantics and transport; P3-08/09 own
concrete implementation and freeze choices. This review does not start them.

If meaningful distinctiveness is still missing at the designated contribution
gate, follow the existing named recurrence rule. Discovering this stronger
antecedent now is a reason to sharpen the future target, not to manufacture
a pass or discard the whole research direction.
