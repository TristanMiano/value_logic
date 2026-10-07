# U03-8a task-certification addendum review

**Scope:** same-model internal mathematical review of the proposed U03-8a supplied by the parent, against the current section 2 assumptions. No scientific execution, clock record, status change, or additional research-time credit.

**Input binding:** `v3/derivations/03_refinement_extensions.md`, whole-file SHA-256 `fb4aad3bc0d5d5d9060beb8f6401b5473b6095cdff833052b5b09058c5ddc31c`; section 2 through the next section heading SHA-256 `aa8d1e1db694abac3f6444493fd6b3a519f6bb63bf36fa3f077e5f76a6e8a36c`. U03-8a was a proposal in the parent message and was not yet in that read section.

## Equivalence: valid

For every finite Boolean template T over the fixed query list Q,

```math
F_\Gamma(Q)\subseteq\{x:T(x)=1\}
\quad\Longleftrightarrow\quad
\Gamma\vdash T(\varphi_1,\ldots,\varphi_k).
```

Provability implies containment by the definition of the represented source. Conversely, for each Boolean assessment x falsifying T, containment says that x is outside the source, so some provable template B_x is false at x. Choose one such template for each of these finitely many assessments. Their conjunction C propositionally entails T: every assessment falsifying T falsifies its selected conjunct. Closure under finite classical propositional consequence therefore yields a Γ-proof of T after substitution. If T is a tautology, there are no falsifying assessments; use the empty conjunction, or directly apply propositional tautology closure.

This argument needs neither a full-model oracle nor a consistency test. It is valid even for inconsistent Γ. Consistency is needed to exclude an empty represented source and the resulting vacuous universal certificates. Intended-truth guarantees still require a separate soundness bridge. This is an elementary finite propositional consequence reconstruction; no stronger logical completeness theorem is being imported.

## Task-predicate construction: valid with explicit data

For a fixed total rational loss on the finite Boolean domain and a known rational threshold, evaluate the predicate at each assignment using exact rational comparison. Its satisfying rows yield a finite Boolean truth-table formula T. Empty and full truth tables need the false and true cases, respectively. Enumerating rows, evaluating losses, constructing and retaining T, and checking the encoding all require work and admitted arithmetic.

For named-action regret, require a fixed named action a, a finite explicit nonempty comparator set A containing a, total rational losses for its members, and a known rational bound r. The predicate can be written semantically as

```math
T_{a,r}(x)=1
\quad\Longleftrightarrow\quad
\ell_a(x)-\ell_b(x)\leq r\text{ for every }b\in A.
```

This is equivalent to pointwise regret against the best action in that same set being at most r. The finite truth table then expresses its uniform version over the represented source. It does not quantify over an unspecified infinite policy class or supply unknown action costs.

The proof certificate is for the compiled Boolean sentence. Interpreting that proof as a loss certificate also uses the checked equivalence between T and the supplied loss predicate. Classical propositional closure alone does not prove arbitrary arithmetic representations, payoff-model adequacy, or the accuracy of learned loss estimates.

## Eventual certification and its limits

If the represented source entails the task predicate, the equivalence supplies a finite Γ-proof. Complete effective enumeration and fair retained checking eventually find it. Alternatively, the finitely many selected consequences form a sufficient finite constraint prefix. Thus a task can be certified while individual coordinates remain unresolved. A provable exclusive-or relation, for example, can fix the loss x_1+x_2 at one without fixing either bit.

This is eventual **positive** certification of source-entailing predicates. It is not a total decision procedure for certifiability, a guarantee for every predicate true only at the intended assignment, or a bounded-time guarantee. Truth-table construction can be exponential, proof search has no supplied useful rate, and finite prototype AST/storage caps can prevent the general construction. Displayed certificates additionally require appropriate publication and source/conflict status handling.

The ordinary proof-enumerator and finite-constraint comparators receive the same construction. The result gives a precise task-specific refinement consequence of the adapter; it does not require full coordinate or source recovery before a useful task certificate and does not itself establish novelty or a Logical Induction performance duty.
