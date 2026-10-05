# F14: primary-source checks and interpretation limits

Contributor: **ChatGPT (GPT-6 Astra Pro)**, October 4–5, 2026.
Evidence type: focused source inspection and protocol reasoning. This is not a
replacement for C4's contribution assessment or F16's fresh reconstruction.
The checked sources informed [F14-v1](../experiments/protocol.md); no final
experimental outcomes were used to select its cutoffs.

## 1. Inspected material and the adopted scope

| Source and inspected locator | Finding used here | F14 decision and exact difference |
|---|---|---|
| Geiger, Lu, Icard and Potts (2021), [Causal Abstractions of Neural Networks](https://proceedings.neurips.cc/paper/2021/file/4f5c422f4d49a5a807eda27434231040-Paper.pdf), sections 2–3 | Causal abstraction and interchange intervention are established methods for comparing high- and low-level computations. | Apply them to expected-cost versus scaled-cost descriptions of an ordinary weighted classifier. Claim only the partial, approximate output relation actually tested. |
| Hewitt and Liang (2019), [Designing and Interpreting Probes with Control Tasks](https://aclanthology.org/D19-1275.pdf), section 2 and sections 3.5–3.6 | A successful decoder can reflect probe expressivity and memorization; control-task comparisons put accuracy in context. | Match subset size, decoder family, proposal count and scoring access. The shuffled continuous-concept procedure is an adaptation, not the paper's word-type random-label construction or a permutation test. |
| Geiger et al. (2022), [Inducing Causal Structure for Interpretable Neural Networks](https://proceedings.mlr.press/v162/geiger22a.html), abstract checked | Training with interchange objectives can induce stipulated structure. | Do not use those objectives in the ordinary model. Expected costs and counterfactual targets enter only after outcome training. No claim is made to reproduce this paper's experiments. |
| Geiger et al. (2024), [Finding Alignments Between Interpretable Causal Variables and Distributed Neural Representations](https://proceedings.mlr.press/v236/geiger24a/geiger24a.pdf), sections 3.2–3.4, Definitions 1–2 | Alignment includes mappings for intermediate variables; constructive abstraction quantifies over inputs and interventions. Distributed rotations can reveal relations that a standard-coordinate search misses. | Test fixed proper coordinate subsets and retain an explicitly narrower per-role output relation. A negative subset search does not exclude distributed abstraction. Overlap and limited multi-donor checks prevent a joint-constructive-abstraction claim. |
| Makelov, Lange and Nanda (2023), [Is This the Subspace You Are Looking for?](https://arxiv.org/pdf/2311.17030), arXiv v2, December 6, sections 3.1–3.3 and Appendix A.3 | A subspace intervention can create a plausible effect through a dormant/cancelled route, complicating attribution to ordinary computation. | The ordinary unused-duplicate witness is necessary but not a universal faithfulness test. Do not infer necessity, uniqueness or complete ordinary-circuit reconstruction merely from patch agreement. The inspected item is the three-author preprint, not an independently checked final conference version. |
| Wu et al. (2024), [A Reply to the “Interpretability Illusion” Arguments](https://arxiv.org/html/2401.12631v1), sections 2–3 and Appendix A | The proposed nullspace criterion can also flag an intuitively relevant variable; the authors defend multiple intervention-relative abstractions. | Do not adopt a blanket nullspace-based rejection rule or present the conceptual debate as settled. State the intervention family and the stronger conclusions left open. |
| Hoeffding (1963), [Probability Inequalities for Sums of Bounded Random Variables](https://www.cs.rpi.edu/academics/courses/spring06/random/hoefding.pdf), JASA 58(301):13–30, printed page 16, Theorem 2 | Independent bounded variables admit exponential tail bounds without an identical-distribution assumption. | Use a conditional-on-discovery two-sided union bound over exactly 560 registered statistics. The inequality is established; its use here is conservative protocol calibration. |
| NumPy, [2.3 random compatibility policy](https://numpy.org/doc/2.3/reference/random/compatibility.html) | Seed equality alone does not promise arbitrary cross-environment stream equality; bit generator, call shape and runtime matter. | Name PCG64 and every stream; pin the numerical version, record environment/data hashes, and avoid a broad cross-host bitwise claim. |
| Phuong and Lampert (2020), [Functional vs. Parametric Equivalence of ReLU Networks](https://research-explorer.ista.ac.at/download/7481/7482/main.pdf), equations (1)–(4), Theorem 1 | The familiar permutation/scaling operations preserve function. The theorem is an existence result for particular networks with non-increasing widths and stated generality conditions. | Use the operations as exact transport controls. Do not apply the theorem as an exhaustive classification of F14's trained 4→32→1 networks. The public institutional copy was inspected after OpenReview returned a browser challenge. |
| Grigsby, Lindsey and Rolnick (2023), [Hidden Symmetries of ReLU Networks](https://proceedings.mlr.press/v202/grigsby23a/grigsby23a.pdf), introduction and section 5 | Parameter redundancy can exceed permutation/scaling; the paper gives mechanisms involving unused activations and restricted hidden images. | Retain a limited gauge-invariance claim. The example below concerns equivalence on a bounded domain, not this paper's global existence theorem or its empirical frequencies. |

The interpretation-illusion exchange was read for the specific inference limit,
not as a new survey of transformer mechanisms. No reported transformer result
is treated as evidence about this small ReLU model. Likewise, an established
method's successful application elsewhere does not establish that F14's
trained models will satisfy the frozen criteria.

## 2. What the primary neural statement actually says

The experiment observes the trained model's ordinary probabilities and its
probabilities after selected coordinate substitutions. It compares these with
one-role expected-cost counterfactuals, matched controls and three specified
cost-scale rivals. The resulting statistical claim is about mean discrepancies
on five defined conditional pair populations, for five specified trained
models. It does not quantify over every hidden activation or intervention.

In particular, the affine raw-cost decoder is diagnostic. It is not a proven
surjective intermediate-variable map, and decoder values after interventions
are not independently admitted by a primary threshold. The exact affine-output
identity instead explains why a successful cost swap would require a
log-cost output contribution on a sufficiently rich exact comparison domain.
An approximate mean probability result is weaker than a uniform logit or
internal-coordinate representation theorem.

There are two distinguishable research aims. One is whether the stipulated
interventions behave approximately like expected-cost substitutions. The other
is whether the identified path is necessary for ordinary output, unique among
all descriptions, or the model's complete algorithm. F14 addresses the first.
The literature exchange above makes the second inference especially important
to avoid. F16 can challenge the significance of the partial relation without
pretending that a different conception of mechanistic explanation was already
proved in F14.

## 3. A small cancellation challenge to the stronger inference

This is a direct illustrative adaptation of ordinary cancelling-path reasoning,
not a claim of a new interpretability theorem. It is a permanent development
example, separate from F14's training task and frozen final population.

For a scalar `t` in `[-1,1]`, take two hidden ReLU units
`h1=h2=ReLU(t+1)=t+1`, with output weights `+1,-1` and zero output bias.
The ordinary logit is identically zero; the output probability is one half.
Removing both contributions leaves every ordinary prediction unchanged.
Now give an illustrative high-level model equal costs
`J0(t)=J1(t)=exp(t)`. Its ordinary optimum is also one half.

Swapping unit 1 from donor `d` into base `b` changes the logit to `d-b`, so
the probability is exactly

    exp(d) / (exp(d)+exp(b)).

This is the proposed J0-only counterfactual. Swapping unit 2 produces `b-d`
and exactly the J1-only counterfactual. The separate roles are disjoint; their
two-donor interventions also compose as their specified high-level costs do.
Thus exact interchange can hold for meaningful changing counterfactuals even
though the pair's net ordinary contribution cancels. Whether one calls this
a useful counterfactual abstraction or an inadequate account of ordinary
necessity is a question about the requested explanatory claim, not a numerical
error that a copied gauge boolean could resolve.

This example is stronger than the unused-zero-output-weight witness in one
respect: its isolated interventions have real effects. It does not show that
the ordinary F14 networks contain a cancelling pair, or that the whole frozen
four-hypothesis statistical gate would pass on this different toy population.
It just blocks the invalid logical implication from intervention agreement
alone to ordinary necessity. Adding an unregistered ablation criterion after
seeing evaluation would change the question; F14 instead freezes the narrower
interpretation prospectively.

## 4. Conditional concentration and selection

Let `D` denote everything used to train models and select candidate subsets.
For each registered statistic, conditional on `D`, the selected intervention
is fixed. Its evaluation rows are independent draws from the frozen stream's
stipulated population. Hoeffding bounds the discrepancy between the sample
mean and its conditional population mean. Applying both tails and a union
bound over `K=560` gives the radius in the protocol. The event bound remains
valid after averaging over discovery, but this does not turn five fixed seeds
into a population estimate over all possible training runs.

The five-stratum comparison is an equally weighted mean of five independent
samples of equal size. The terms need not be identically distributed: their
expectations average to the declared mixture target and their common bounds
give the same inequality. Sharing intended pairs between two hypotheses makes
the errors paired, which is useful for comparison. Dependence between different
statistics does not invalidate a union bound. Reusing one donor pool via a
permutation would introduce dependence between rows of a statistic; that is
why the incorrect-donor control instead uses independent generated records.

Candidate search is already conditioned on independent discovery data. Its
128 proposals do not each become a final confidence claim. In contrast, the
four hypotheses, two roles, five strata, multiple controls and five models are
all potential simultaneous conclusions and are counted explicitly. The extra
conditional-base calibration rows close a real failure mode: ordinary-input
accuracy need not extend to a conditioned intervention population. By the
pointwise triangle inequality, their .05 upper bounds plus .05 intervention
bounds imply .10 mean absolute adjusted-effect bounds without an additional
statistical family. They do not imply .10 RMSE or a per-example guarantee.

These confidence statements assume the stipulated pseudo-random streams serve
as independent sampling draws. They do not validate the real-world source
model, prove the numerical implementation, or warrant stopping/restarting a
run until an interval happens to pass. The fixed sample counts, stream registry,
complete-result requirement and retained failure records are separate controls.

## 5. Contribution comparison and unresolved obligations

The exact object of F14's methodological adaptation is the experiment contract:
consumer-specific retention and current proof reception are compared with
ordinary exact methods under declared information and costs; a small
outcome-trained classifier is tested against cost and normalized-probability
interventions with matched search, numerical transport and prospective error
criteria. None of its ingredients is presented as an invented general method.

The magnitude of the adaptation is deliberately bounded. It can support
reproducibility, clear falsifiers and a useful application demonstration. A
newly coded protocol or a local counterexample is not by itself a supported
novel contribution. The substantive C4 synthesis/application assessment stays
at its existing inspected-antecedent scope pending the result and F16.

Named later obligations are: interpret F15 under the fixed criteria; reconstruct
the strongest ordinary combined baseline and the meaning of source-row
composition in F16; challenge whether any positive partial neural relation
adds meaningful explanatory value; and reopen R-N01-01 if the scoped
contribution is displaced. No new worldwide-priority, necessary-circuit,
sample-optimality, deployment or performance claim is closed here.

## 6. Gauge controls are not an exhaustive equivalence class

The two symmetry sources above separate operations that always preserve a
network's function from the stronger classification of all parameters with
that function. Phuong and Lampert's Theorem 1 has an existential quantifier and
architectural/generality conditions. Neither it nor the hidden-symmetry paper
turns F14's transported-control check into unique parameter identification.
The 4→32 widening alone prevents directly invoking the former architecture
condition. F14 also works on a bounded input domain, where always-active
units can expose extra affine freedom.

Here is a direct elementary example, constructed during F14 development.
It is not the F14 outcome-learning task or a new theorem claim. On
`(x1,x2) in [-1,1]^2`, let

    h1 = ReLU(x1+2), h2 = ReLU(x2+2), z = h1-h2 = x1-x2.

With `A=[[1,1],[0,1]]`, a second two-unit ReLU network has

    h1' = ReLU(x1+x2+4), h2' = ReLU(x2+2), z' = h1'-2h2'.

All four preactivations are positive throughout the domain. Thus `h'=A h`
and `z'=z` there. This is a non-monomial mixing, not a permutation followed
by positive diagonal scaling. The two implementations give the same ordinary
sigmoid output at every domain point.

For base `b` and donor `d`, swapping the first original coordinate gives
`z_I=d1-b2`. Swapping the first new coordinate gives instead
`z_I'=d1+d2-2b2`. With `b=(0,-1)` and `d=(0,1)`, those logits are `1` and `3`.
The corresponding probabilities differ by approximately `.2215`, despite
exact ordinary equivalence. Transporting the original intervention requires
the oblique projector

    A diag(1,0) A^-1 = [[1,-1],[0,0]],

applied to the hidden donor-minus-base difference. That transported update
recovers the original effect; it is not replacement of the same single new
coordinate. The equalities are algebraic over the domain, not inferred from a
finite validation grid.

This establishes a useful boundary for interpreting F15: gauge transport
checks implementation consistency for the declared operations; coordinate
search tests a particular representation class within its fixed budget. It
does not establish invariance under all domain-preserving functional
reparameterizations. A richer intervention class could be evaluated in later
work with a new prospective search/complexity contract, after recording F15's
original result. It is not silently added to rescue a negative outcome.
