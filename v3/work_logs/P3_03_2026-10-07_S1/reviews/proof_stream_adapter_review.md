# U03-8 proof-stream adapter review

**Scope:** same-model internal mathematical review of section 2 and its dependence on section 1 of `v3/derivations/03_refinement_extensions.md`. No scientific execution, clock record, or additional research-time credit. This reviews the mathematical adapter, not an implementation.

**Input binding:** whole-file SHA-256 `16c7b2ca1aeaae9e314c49d43c6c257382e78c7efd947bb22675080314da57bd`; sections 1–2, from the `## 1.` heading up to but excluding `## 3.`, SHA-256 `c8120824b26db71b1889bf231de6d2b9004ce5ae7b88a5a10d7b8fc1cee9484e`.

## Verdict and two local qualifications

The source-intersection equality and finite-fragment stabilization argument are valid. The consistency-to-nonemptiness proof is also valid and needs no model or consistency oracle. Two conclusions should carry their premises explicitly:

1. Change the singleton sentence to **“If Γ is consistent and proves each sentence in Q or its negation …”**. Without consistency, a classical theory can prove both signs; the source is then empty, not a singleton. The consistency condition in the preceding paragraph is not syntactically attached to this later conditional.
2. The sentence promising eventual exact extrema should say **“when the limiting source is nonempty; otherwise exact filtering eventually reports conflict.”** Section 1 already imposes nonemptiness, and section 2 later handles conflict, but repeating this premise at the displayed-result conclusion prevents an unconditional numerical reading.

## Effective proof enumeration

For precision, the proof relation should satisfy

```math
\Gamma\vdash\psi\quad\Longleftrightarrow\quad
\exists\pi\;\mathrm{Check}_\Gamma(\pi,\psi)=1,
```

with decidable checking on finite codes. Here checker soundness is **syntactic**: an accepted certificate is a valid Γ derivation. It is not the separate assertion that Γ is true in the intended interpretation. Decidability and one-way soundness alone would permit an always-rejecting checker; coverage of genuine derivations is also required. The draft's enumeration and eventual-service hypothesis supply that coverage when “proof” refers to this certificate system.

For effectively enumerable axioms, a finite record can give the axiom enumerator's finite run witnessing each axiom use. Checking that run is computable; it does not decide membership in the entire axiom set. This needs an effective syntax and fixed enumerator, which are natural explicit parts of the proposed adapter.

The marked pair construction is appropriate: retain the Boolean template and check that the proof conclusion is its exact syntactic substitution. It requires neither recovering a template from an arbitrary sentence nor deciding logical equivalence. Dovetailing all finite candidate pairs with retained checker progress covers every valid pair. All generation, checking, retention, and filtering remain work.

To avoid an indexing ambiguity shared with section 1, define the finite received prefix at stage n as **all accepted constraints by finite computational stage n**, allowing repeated prefixes. A stream may have no next actual receipt. Indexing by the ordinal number of actual receipts alone does not guarantee a total computable function returning every requested prefix. Stage indexing makes the construction total without assuming that another proof or informative receipt will arrive.

## Why the positive theorem holds

Every admitted template is provable, so every assessment in the metatheoretically defined source survives admission. Conversely, an assessment outside that source violates some provable template. Its marked proof pair is eventually checked, excluding that assessment. These two inclusions prove equality of the limiting received source and the represented proof-consequence source, even when both are empty.

For nonemptiness under consistency, suppose the source were empty. For each of the finitely many Boolean assessments, select one provable template it violates. Their finite conjunction has no Boolean satisfying assignment. Classical propositional closure lets Γ derive that conjunction and the substituted propositional consequence that it is contradictory. This contradicts Γ-consistency. This metatheoretic argument does not ask the running method to certify Γ-consistency or construct a full Γ-model. Only a separate semantic soundness premise places the intended answer vector in the source.

The finite domain then gives eventual stabilization. Eventual exact displayed extrema additionally require the paid exact filtering, admitted arithmetic, nonemptiness, and eventual publication of sufficiently advanced prefixes specified in section 1. Fair proof discovery alone does not establish the display claim.

## Strongest supported scope

For a fixed effective proof system and fixed finite query fragment, the adapter eventually represents all provable Boolean consequences exactly; under consistency it retains a nonempty set of assessments. With the processing and publication conditions, every fixed admitted total rational loss eventually receives its exact extrema over that set. No computable stopping signal, useful rate, intended-truth identification, or Logical Induction performance duty follows here.

Unbounded proof lengths, templates, and certificate processing are outside the current VM's finite syntax, input, and receipt caps. The text correctly presents this as a mathematical adapter. An ordinary proof enumerator plus finite Boolean constraint engine obtains the same result under the same access and cost conditions; the review supports no priority claim or change to P3-N01.
