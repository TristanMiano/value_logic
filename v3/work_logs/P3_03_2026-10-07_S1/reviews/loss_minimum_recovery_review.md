# U03-12 loss-minimum recovery review

**Scope:** same-model internal mathematical review of section 6 of `v3/derivations/03_refinement_extensions.md`, plus the subsequently supplied finite rational-domain extension proposal. No scientific executions, status changes, clock records, or additional research-time credit.

**Read version:** whole-file SHA-256 `26a729725f3feaecb299c070d70f7b856ccf3f88f09bf4e69d1b2aa8cf55d0c6`; section 6 through end of file SHA-256 `1b522b8fcd8187b550d6b9721776863c21990f0a0cfc4f5c01ea8b63c93e0fe2`. The proposed PWA extension was supplied in the parent message after this read; it is not part of that content binding.

## Boolean result: valid, with one wording correction

The assumptions are a known finite Boolean candidate domain, a nonempty source F contained in it, known semantic unit stakes, and an exact minimum service for each specified loss. Hamming loss is nonnegative and integer valued, vanishing only at its named candidate. Consequently its minimum is zero exactly for source members and at least one otherwise. The complete family therefore recovers F. Each row has linear expression size; the full family has exponentially many rows. Neither statement supplies minimization, admissible VM capacity, or query processing for free.

Specify that approximation error is **absolute**. If every estimated minimum differs from its true minimum by strictly less than one half, thresholding at one half separates the two cases. At error one half the one-bit minima zero and one can both yield an estimate of one half. Known positive stake scaling gives the stated scaled gap; a claim about the native rational grammar additionally requires an admitted rational stake and arithmetic.

The sentence saying inclusion “needs a valid witness or an exact attained minimum” should allow the following paragraph's gap certificate. A certified upper bound on the true minimum below one already forces membership, without the service returning a witness or exact minimum. Suggested wording: **a zero structural lower bound alone gives no inclusion certificate; inclusion needs additional information forcing the true minimum to zero, such as a valid witness, an exact minimum, or a gap-resolving error bound.** An interval enclosing all point losses and an interval certified to enclose the minimum have different meanings.

## Expected losses and ordinary comparison

Under one normalized law, the same Hamming rows retain exactly the coordinate means. They depend only on those means; conversely, writing r_z for the row expectation gives

```math
E[X_j]=\frac{1+r_0-r_{e_j}}{2}.
```

For two or more coordinates this need not determine dependence. The two equal-mixture examples in the text have the same means and all four row expectations equal to one; their minimum families distinguish their support sets. No probability weights are inferred by the minimum service. The credal comparison is correct when “all laws supported on F” allows every distribution with support contained in F, including point masses: its lower expectation is exactly the pointwise minimum.

This is an elementary distance-to-set recovery construction and ordinary lower-expectation calculation. In geometric terms, affine extrema generally determine only the convex hull. Every Boolean candidate is an exposed vertex, which lets the chosen affine rows recover its membership. On the non-Boolean candidate domain {0, 1/2, 1}, the sources {0,1} and {0,1/2,1} have identical extrema for every affine loss. This is a useful limitation to add; it does not contradict the Boolean theorem.

## Proposed finite rational-domain PWA extension

The proposal is valid for a known finite set Z of distinct rational vectors and a nonempty F contained in Z. The loss

```math
D_z(x)=\sum_j\max(x_j-z_j,z_j-x_j)
```

uses rational affine terms and finite max/sum operations, and vanishes exactly at z. If Z contains alternatives to z, their finitely many positive distances have a positive rational minimum δ_z. Thus the same membership argument works, and absolute minimum error strictly below δ_z/2 suffices. For a singleton Z, nonemptiness already determines F; do not take a minimum over the empty alternative set.

Enumerating Z, computing and representing the gaps, retaining the loss descriptions, and obtaining their minima all require work. Gaps need not have a uniform positive lower bound across different rational candidate domains. This extends the mathematical loss-query family, not the current Boolean VM. In contrast with affine losses, these PWA queries distinguish the interior candidate in the preceding counterexample.

Do not carry the Boolean expectation claim over unchanged: expected absolute deviations depend on coordinate distributions, not just their means. On Z={0,1/2,1}, the center loss expectation identifies the center mass, and the endpoint loss expectation then separates the endpoint masses. Those richer rows and normalization recover that three-point law. P3-02's finite loss-matrix criterion controls the general probability-recovery question.

The result supports a precise comparison of supplied information services and a scoped adapter. By itself it establishes neither a new recovery theory nor superiority to ordinary finite optimization or credal methods. Full source recovery remains optional when the consumer's particular loss or decision requires less information.
