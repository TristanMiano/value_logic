# F15-ND01: representation assumptions and diagnostic interpretation

Author: ChatGPT (GPT-6 Astra Pro), representation-analysis subagent, 2026-10-05.
Status: explanatory analysis and proposed diagnostic interpretation. No new
training or numerical results are produced by this note. F15's frozen outcome
and contribution dispositions remain unchanged. Concurrent subagent work adds
zero minutes to the root clock.

## Salient interpretation

**Ordinary training gives the network no task-specific reason to organize its
features into one clean eight-neuron block for each expected cost.** The loss
rewards the final predictions; it does not reward that internal decomposition.
Useful information could instead be distributed across neurons, mixed with
other input factors, or represented through a different decomposition of the
same computation. The intervention probe therefore tests whether the learned
organization is sufficiently accessible to this particular extraction family,
as well as whether the network learned the task. Feature mixing is a plausible
explanation for F15's incomplete correspondence. It has not yet been identified
as the cause in these five models. See the [frozen neural design](../neural_design.md)
and the primary literature below.

This is the familiar interpretability difficulty the user asked to make
salient. **Technical superposition is a more specific hypothesis.** In the
terminology of Elhage et al., it involves representing more feature directions
than available dimensions, with interference. A distributed code can exist
without that compression. Our results establish neither the requisite feature
count nor superposition in the five networks. “Mixed or distributed features”
is the supported description of the hypothesis; “demonstrated superposition”
would overstate the evidence. [TOY]

## Why the restriction matters in this exact task

The following algebra specializes the implemented
[`loss_and_gradients`, `high_prediction`, and `_swap_probabilities`](../neural.py).
It does not posit another training objective.

Let `eta = P(Y=1|x)`, `J0=cFN*eta`, and `J1=cFP*(1-eta)`.
For an output probability `p`, conditional expected weighted cross-entropy is

\[
L(p)=-J_0\log p-J_1\log(1-p).
\]

Since

\[
L'(p)=-J_0/p+J_1/(1-p),\qquad
L''(p)=J_0/p^2+J_1/(1-p)^2>0,
\]

the unique optimum is

\[
p^*=\frac{J_0}{J_0+J_1},\qquad
z^*=\operatorname{logit}(p^*)=\log J_0-\log J_1.
\]

Equivalently,

\[
z^*=\log c_{\rm FN}-\log c_{\rm FP}
      +\log\eta-\log(1-\eta).
\]

Thus price-related contributions and a shared probability-related contribution
could suffice. The ordinary objective constrains their total, not their
allocation to separate cost modules. Algebraically, adding any function to one
contribution and subtracting it from the other preserves that total. This
underidentification argument does not assert that every such decomposition is
representable by this fixed finite network. ReLU also privileges neuron axes;
arbitrary hidden rotations are not an exact parameter symmetry of a ReLU layer.
Neither qualification supplies a requirement for this particular cost partition.

For the fixed affine head, write

\[
z(x)=\beta+v^T h(x),\qquad
\phi_S(x)=\sum_{i\in S}v_i h_i(x).
\]

Swapping coordinates `S` from donor `d` into base `b` gives exactly

\[
z_{S\leftarrow d}(b)=z(b)+\phi_S(d)-\phi_S(b).
\]

Define the signed contributions
`ell_0(x)=log J0(x)` and `ell_1(x)=-log J1(x)`, baseline logit error
`e(x)=z(x)-z*(x)`, and residual `r_S(x)=phi_S(x)-ell_r(x)` for role `r`.
The ideal role intervention has logit
`z_H=z*(b)+ell_r(d)-ell_r(b)`. Therefore

\[
\boxed{z_{S\leftarrow d}(b)-z_H
       =e(b)+r_S(d)-r_S(b).}
\]

This separates imperfect ordinary prediction from imperfect isolation of the
target contribution. A good scalar decoder of `Jr` does not establish that the
fixed output-weighted subset contribution approximates the required signed
log-cost. Because sigmoid has derivative at most `1/4`, the absolute probability
error is at most one quarter of the absolute right-hand side. This is a bound,
not an equality or a new F15 criterion.

If the base logit is exact and interchange equality holds on all pairs of a
connected comparison domain, `r_S` must be constant there. F15's finite,
conditioned comparisons establish no global representation theorem. A finite
ReLU sum is piecewise affine, so the frozen design appropriately required
approximation, rather than exact equality to logarithms on a continuous domain.

For equal-target pairs, `ell_r(d)=ell_r(b)`. A nonzero actual swap effect
directly exhibits failure of target invariance for that selected subset.
F15 reports output-effect RMS **0.029847–0.052271** across the model/role rows
([results, neural diagnostics](../results.md)). This motivates investigating
feature leakage. It does not rule out another subset or another intervention
family. The complete 0/5 result additionally contains control-superiority and
scale-discrimination requirements; it is not solely a test for representation
existence.

## What a continuous relaxation could resolve

Hold the trained network, its original output weights, and the diagnostic
input pairs fixed. Three questions should stay separate:

| Diagnostic | Quantity assessed | Interpretation of improvement |
|---|---|---|
| More coordinate search | `phi_S`, with exactly eight selected coordinates | Evidence that the original search left attainable subset performance undiscovered. |
| Fractional-mask intervention | `h'=h_b+m*(h_d-h_b)`, `0<=m_i<=1`, `sum(m)=8` | Tests a larger, explicitly defined intervention family containing all size-eight masks. Improvement implicates the hard-mask restriction, subject to matched fitting and validation. |
| Unconstrained linear contribution | `a^T h` fitted to a signed log-cost or target logit difference | Tests available linear prediction capacity. Success alone establishes neither an admissible subspace interchange nor native causal use. |

A fractional mask has logit change
`sum_i m_i*v_i*(h_i(d)-h_i(b))`. Its logit-error objective can include the
baseline error exactly by fitting the target `z_H-z(b)`. The resulting least
squares objective is convex in `m` under the stated linear bounds and sum
constraint. Actual probability error should still be reported. These are
proposals for development, not amendments to F15 or claims that the relaxation
has been run.

For comparison, an orthogonal-subspace interchange acts as

\[
h'=h_b+P(h_d-h_b),\qquad P=P^T=P^2,
\]

so its output effect is `(Pv)^T(h_d-h_b)`. If `a=Pv`, necessarily
`a^T v=||a||^2`. An arbitrary fitted readout vector need not satisfy this
condition. Even when one suitable projector exists, output behavior with a
single scalar head cannot uniquely identify all its internal action. A
successful unconstrained readout relaxation must therefore be reported as
capacity evidence, followed by a separately specified intervention test.

Distributed alignment search (DAS) is a relevant established next method: it
learns a change of basis and swaps subspaces while keeping the network fixed.
Its motivating example explicitly separates good task behavior from a failed
coordinate alignment and a successful rotated alignment. It does not imply
that these five networks admit the desired cost decomposition. [DAS]

## Primary sources and comparison scope

- **[DAS]** Atticus Geiger, Zhengxuan Wu, Christopher Potts, Thomas Icard,
  and Noah D. Goodman, *Finding Alignments Between Interpretable Causal
  Variables and Distributed Neural Representations*. First submitted
  2023-03-05; version 4 dated **2024-02-21**.
  [Pinned full text](https://arxiv.org/html/2303.02536v4),
  [version record](https://arxiv.org/abs/2303.02536v4).
  Read beyond the abstract: §§3.4–3.5 (distributed interventions and alignment
  search), §4.4 (random-network analysis), and §§5.3–6 (results and limits of
  interpreting the learned structure). The random-network analysis also
  motivates retaining controls when the intervention family is enlarged.
- **[TOY]** Nelson Elhage, Tristan Hume, Catherine Olsson, Nicholas Schiefer,
  Tom Henighan, Shauna Kravec, Zac Hatfield-Dodds, Robert Lasenby, Dawn Drain,
  Carol Chen, Roger Grosse, Sam McCandlish, Jared Kaplan, Dario Amodei,
  Martin Wattenberg, and Christopher Olah, *Toy Models of Superposition*,
  Transformer Circuits Thread, **2022-09-14**; arXiv version 1 submitted
  **2022-09-21**.
  [Article](https://transformer-circuits.pub/2022/toy_model/index.html),
  [author-hosted full PDF](https://transformer-circuits.pub/2022/toy_model/toy_model.pdf),
  [version record](https://arxiv.org/abs/2209.10652).
  The article's HTML retrieval failed; the full PDF was read instead:
  “Definitions and Motivation,” “The Superposition Hypothesis,”
  “Demonstrating Superposition” (setup and results), and “Theories of Neural
  Coding and Representation.” The experiments use synthetic sparse features;
  they are not measurements of F15's dense four-input classification problem.

These sources supply established framing and methods. This note claims an
application of those ideas to the frozen probe, not a new theory of
superposition, a new alignment method, or a worldwide-priority result.
