# Conditional-edit certificates: useful reduction, established machinery

Codex (GPT-6), DEVELOPMENT. This short screen prevents turning an ordinary
explanation algorithm into a claimed new general mechanism.

Fix a checked original source F, target G, transformation T_b and an actual
world x in F for which T_b(x) belongs to G. Let U_b contain the unsafe original
worlds y in F with T_b(y) outside G. A set J of queried coordinates certifies
this transformation on x exactly when it intersects every difference set
Delta(x,y)={i:x_i differs from y_i}, y in U_b. The proof is direct: an unsafe
world survives the observations iff no observed coordinate distinguishes it.
Restrict the difference sets to purchasable coordinates; an empty set proves
that the action cannot be certified through this interface. Minimum fees are
therefore a weighted hitting-set problem. Its fractional relaxation gives a
lower bound, and an integral hitting set gives a sufficient query certificate.

This is an explanatory certificate for a KNOWN x. A live reasoner does not
know which literals it will purchase, so selecting the cheapest explanation
after seeing x is not an implementable online acquisition policy. Adaptive
acquisition is a decision tree over possible answers and may be much more
expensive. Likewise a promising edit need not help the actual value objective,
as the uf50-02 and uf50-03 results show. Balanced model splitting and minimal
certificates solve different objectives; neither is automatically best for
costed regret.

[Ignatiev, Morgado and Marques-Silva (2016)](https://arxiv.org/pdf/1604.08229),
section 2.2 Definition 1 and section 2.3 Algorithm 2, formulate minimum-cost
propositional explanations and implicit hitting-set construction. Setting
background T=F, manifestation M=G composed with T_b, and hypotheses to the
observed literals supplies the present adapter. [Ignatiev et al.](https://arxiv.org/pdf/2012.11067),
section 3 Propositions 1--2 and Theorem 1, make abductive/contrastive explanation
duality explicit. These are strong ordinary antecedents, not merely distant
analogies. Park a stand-alone "new certificate selector" claim; no new benchmark
is justified just to reproduce the reduction.

[Marques-Silva, Janota and Lynce (2010)](https://sat.inesc-id.pt/~mikolas/ecai10.pdf),
sections 2.2 and 3.1--3.3, define backbone literals and discuss model filtering
and persistent SAT calls. This explains why a paid query of a forced literal
does not refine the logical source, and why native reuse must be a control.
The paper's empirical scale does not transfer to our implementation.

[Shortest reconfiguration paths in Boolean formulas](https://arxiv.org/html/1404.3801v1),
introduction and token-system definitions, concerns paths whose intermediate
single-bit flips remain valid. Our atomic terminal batch is a different
contract. [Model and Program Repair via SAT Solving](https://arxiv.org/pdf/0710.3332),
section 3 Definitions 2--4, repairs a transition structure to satisfy a temporal
specification. This is prior repair machinery, not the same paid-observation
problem. Neither distinction establishes novelty by itself.
