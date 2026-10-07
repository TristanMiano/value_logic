# Review: shared uncertainty versus local natural extension

2026-10-07. Reviewer: **ChatGPT (GPT-6 Astra Pro)**, independent same-model reconstruction. Scope: [imprecise-tree source note](imprecise_tree_source.md), especially its finite calculation and Theorem 7 boundary. P3-01 only.

**Disposition:** the calculation and stated source distinction are correct. Two concise qualifications would make the import and decision claims fully explicit: name the upper-expected-loss decision criterion and retain Proposition 2.7's hypotheses. No new theorem or experimental result is warranted.

## 1. Independent finite reconstruction

The shared mixture gives

```
R_theta(00,01,10,11)
  = (theta/2, (1−theta)/2, (1−theta)/2, theta/2).
```

Both `X` events have probability `1/2` for every admissible `theta`, including the endpoints. Therefore every displayed conditional is defined. Direct division gives

```
a := P(Y=1 | X=0) = 1−theta,
b := P(Y=1 | X=1) = theta,
E[Y] = (a+b)/2 = 1/2.
```

The original family is the line `a+b=1` in the square `[0,1]^2`. Each coordinate separately ranges from zero to one, but its minimizer or maximizer need not use the same `theta` as the other coordinate. Replacing the line by independent local choices fills that square. Its joint laws are

```
((1−a)/2, a/2, (1−b)/2, b/2).
```

Its lower expected `Y` cost is zero, attained at `a=b=0`; its upper is one, attained at `a=b=1`. Neither extremal law belongs to the original family. Thus the conditional-envelope calculation discards the shared constraint, rather than contradicting linear expectation or conditional probability.

With fixed actions having losses `Y` and `3/4`, **minimizing worst-case expected loss at the root** selects the first action for the original family (`1/2 < 3/4`) and the fallback for the larger family (`3/4 < 1`). This is exactly the source note's numerical conclusion.

**IT01 — name the criterion and timing.** “Robust choice” should be expanded to the bold phrase above. Other robust criteria need not agree. For example, over the enlarged family, the worst regret of the `Y` action is `1/4`, whereas the fallback's is `3/4`; minimax regret would select `Y`. Moreover, after observing a particular `X`, the original family's conditional `Y` probability still ranges over `[0,1]`, so a newly made conditional upper-loss decision can prefer the fallback too. The root comparison concerns the declared action/commitment service; it does not establish universal agreement of all conditional decision rules.

## 2. Primary-source boundary

Independently inspected [arXiv PDF](https://arxiv.org/pdf/0801.1196), whose first page identifies **0801.1196v1, 8 January 2008**. In §4.1, p.11, local assessments are held at the root. Theorem 3 (§4.2, p.13) constructs their smallest D1–D4/D5' extension; §4.3 defines its predictive previsions. Theorem 7 (§4.5, p.15) concerns those previsions and ordered cuts, not arbitrary supplied global families. The §9 discussion, p.23, explicitly ties concatenation equality to that local-model construction. The source note preserves this distinction correctly.

**IT02 — preserve the general inequality's conditions.** Proposition 2.7, p.9, requires the relevant partition-conglomerability; its footnote also requires well-defined quantities. “General composition gives an inequality” should retain that qualification if used as a stand-alone import. In the finite two-branch fixture, direct arithmetic already establishes the comparison without a broader theorem import.

This review does not claim that every global family lacks an exact recursive representation. Retaining the shared parameter or another sufficient global dependency could change the interface and its cost. It also does not identify conditional-envelope enlargement as an error when the enlarged uncertainty model is openly intended.

## 3. Verification scope and resources

The fixture was checked by algebra only. No experiment, executable numerical test, learner or P3-02 work was started. Selected primary statements were inspected, not all appendices or the entire proof chain. Reviewed source-note SHA256: `6e8b0a831951d6e2b9e4c41d2b9f40447e0ebaf8e7b169f4b68e93f203de7661`.

One source-retrieval failure occurred: opening the version-suffixed arXiv PDF returned `DisabledError`. Opening the unsuffixed PDF succeeded and displayed the required v1 identifier; no substitute version was silently assumed. Only this review note was written. No canonical or clock edits and **zero principal time credit**. Own engaged duration, inference tokens and dollar cost are unmetered/unknown.
