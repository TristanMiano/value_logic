# Gate C principal primary comparison

Contributor: **ChatGPT (GPT-6 Astra Pro)**. Accessed October 6, 2026 UTC.
This is bounded primary reading used to check a concrete contribution
objection. It is not a fresh full literature review or external peer review.

## Sources directly read

**Mahmood Ettehad and Simon Foucart, _Instances of Computational Optimal
Recovery: Dealing with Observation Errors_ (2021), DOI 10.1137/20M1328476.**
[Author PDF](https://foucart.github.io/publi/OR_Uncertainty_v2.pdf), introduction
and §2.1 through Theorem 1's duality proof, PDF pages 1-5. The theorem provides
a linear program for an ambient vector minimizing worst-case target error
over a polytope constrained by observations. The simplex and exact old means
fit this formulation. It supplies an established computational solution, not
the reset-family compatible-center construction. Original web locator:
`turn76view0`. No claim to have audited later polynomial/semidefinite sections.

**Pradyumna Paruchuri and Debasish Chatterjee, _A numerical algorithm for
attaining the Chebyshev bound in optimal learning_ (arXiv:2307.01304v1,
July 3, 2023).** [Primary HTML](https://arxiv.org/html/2307.01304v1), introduction,
equations (1)-(2), §2's finite-dimensional formulation and the setup through
(13). The relative-center problem restricts the candidate output set;
its formulation therefore already captures the distinction between free
and constrained centers. It does not state F16-C1's reset-family equality
or endpoint/adjacent-level construction in the inspected passages. No new
validation of this paper's broad algorithmic or complexity claims is asserted.
Original web locators: `turn76view1`, `turn77view0`.

## Project inference

F16-C1 proves that the compatible-output restriction costs no additional common
worst-case error for a particular complete exact old-summary fiber family,
and gives an explicit law. This is an application-specific consequence beyond
posing or numerically solving the generic optimization. The source-restricted
triangle in F16 explains the gap: normalized free radius 1/2 versus compatible
radius 2/3. No generic convex-set assertion can make them equal.

This supports the modest specialized application/formal-adaptation assessment
relative to those formulations. It does not establish worldwide priority or a
general computational advantage. The ordinary method may use the same formula.

Other antecedents, including incremental abstraction-carrying code and the
unavailable 2022 Choquet-identification section, are covered by the
[separate contribution source record](reviews/contribution/source_record.md)
and the attributed C4/F16 readings. The principal did not repeat those searches
or represent prior reading as fresh. Failed access adds no favorable evidence.
Web content was read through the retrieval tool; no invented source-file hash
is supplied.
