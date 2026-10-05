# ND01: principal source checks and interpretation boundary

Contributor: ChatGPT (GPT-6 Astra Pro), 2026-10-05. These are principal-agent
reading notes; collaborator reading is not added to the principal clock.
This note accompanies a development diagnostic and does not amend either
experimental freeze. It is a bounded method comparison, not a worldwide
priority search.

## Sources actually inspected

1. **Geiger, Wu, Potts, Icard and Goodman, _Finding Alignments Between
   Interpretable Causal Variables and Distributed Neural Representations_.**
   [Version 4, 2024-02-21](https://arxiv.org/html/2303.02536v4),
   especially §§3.4–3.5, 4.4 and 5.3–6. The rotated linear example establishes
   why successful task behavior need not admit a coordinate alignment. DAS
   searches an orthogonal change of basis with the underlying network fixed.
   The random-network and further-decomposition analyses qualify what an
   alignment means. The reported best-of-three alignment training results
   must not be relabeled as a general held-out success guarantee.

2. **Elhage et al., _Toy Models of Superposition_ (2022).**
   [Author-hosted full PDF](https://transformer-circuits.pub/2022/toy_model/toy_model.pdf),
   definitions on PDF pages 5–7 and discussion on page 48. The distinction
   between an ordinary distributed code and feature compression with
   interference matters here. The paper's sparse toy-feature setting supplies
   a hypothesis and vocabulary; it does not establish superposition in our
   four-input, 32-hidden-unit networks. A non-coordinate explanation needs no
   claim about more features than dimensions.

3. **Makelov, Lange, Geiger and Nanda, _Is This the Subspace You Are Looking
   For? An Interpretability Illusion for Subspace Activation Patching_,
   ICLR 2024.**
   [Official conference PDF](https://proceedings.iclr.cc/paper_files/paper/2024/file/70b8505ac79e3e131756f793cd80eb8d-Paper-Conference.pdf),
   §§3–5, PDF pages 4–8. Patching can combine a varying output-disconnected
   component with an output-sensitive dormant component. The paper also
   presents a more faithful success case and additional circuit evidence.
   The conference author list includes Geiger; an older preprint's shorter
   author list should not be substituted for this version.

4. **Wu, Geiger, Huang, Arora, Icard, Potts and Goodman, _A Reply to Makelov
   et al. (2023)'s “Interpretability Illusion” Arguments_, 2024-01-23.**
   [Version 1 full text](https://arxiv.org/html/2401.12631v1),
   [PDF](https://arxiv.org/pdf/2401.12631), §§2–4 and the §5.2 comparison.
   The reply shows that a downstream-nullspace test can reject an otherwise
   intuitive alignment. It emphasizes the input-induced activation geometry,
   multiple abstractions, meaningful high-level counterfactuals and disjoint
   training/evaluation examples. Its criticism of a weak output-effect metric
   is relevant to keeping probability error and decision disagreement visible.

The HTML retrieval for the superposition article failed, so the PDF was used.
Early arXiv full-text opens for the illusion paper and an incorrect `v2` URL
for the reply failed; the official conference PDF and the reply's actual `v1`
links resolved. One domain-restricted search returned irrelevant university
home pages and was not used as evidence. These were literature retrieval
failures, not scientific attempts or missing experimental observations.

## Application to this diagnostic: our reasoning

**Ordinary training gives the network no task-specific reason to organize its
features into one clean eight-neuron block for each expected cost.** The
ordinary loss constrains the final answer, leaving its internal organization
underdetermined. F15 therefore challenged both task learning and accessibility
to a particular extraction family. Mixed features, a different basis or a
different computational decomposition are plausible explanations. “These
networks demonstrably use superposition” would go beyond the evidence.

ND01's improvement with unchanged networks supplies local evidence that the
original extraction procedure left useful correspondence undiscovered. The
same-objective exhaustive binary and fractional comparison further tests the
hard-mask restriction. Neither comparison identifies a unique utility or a
unique set of causal features. The mechanism note derives why fractional
logit averaging can reduce error and why output-equivalent projectors may be
constructed along unused activation directions.

The final source check keeps two different nullspaces separate. Our whole-box
certificate uses the orthogonal complement of **activation differences**;
the patching debate also studies the kernel of **downstream computation**.
For the stored scalar heads the latter has dimension 31, whereas our certified
inactive difference directions number two or three. They are not the same
space. An argument concerning one must not silently be substituted for the
other. DAS also learns its alignment from high-level intervention targets;
it does not make ordinary task training an unsupervised cost-feature discovery
procedure. ND01 likewise used explicit cost-derived discovery targets while
leaving ordinary network training unchanged.

The two papers debating patching should not be treated as establishing a
blanket rule that any such projector is invalid. Their disagreement is
precisely why our stronger claim remains narrow: the observed outputs alone
do not identify native feature organization. To investigate a joint cost
abstraction, another protocol would have to specify its intervention algebra,
metric, controls, generalization population and acceptance rule in advance.
Individual good output changes and joint compositional behavior are separate
questions. A frozen, auditable test of the latter could add explanatory
evidence even if it again produced a negative result.

## Contribution comparison

Coordinate-versus-distributed accessibility, fractional optimization,
activation patching and the interpretation problem all have established
antecedents. ND01's contribution is a local diagnostic application and a
formal specialization to this finite affine-head cost task. The additional
algebra has not been subjected to a priority search and is not presented as a
new general theorem of mechanistic interpretability. The bounded C4-S
synthesis/application claim remains separately assessed; a positive neural
result was never a prerequisite for it.
