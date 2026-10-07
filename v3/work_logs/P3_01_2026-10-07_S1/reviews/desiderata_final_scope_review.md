# P3-01: final desiderata scope review

Reviewer: **GPT-6 Astra Pro**, `/root/p301_induction_sources`.
Date: **2026-10-07 UTC**. Distinct same-model internal, nonblind review.
Scope: U05–U09/V01/F01 against the current problem contract and the already
completed LI import audit. No new theorem import, broad source reread,
canonical/control/clock edit, publication or concurrent principal time credit.

**Disposition:** no inspected row presently asserts a supplied LI theorem as
a current implementation guarantee. The opening prospective status, U05's
explicit non-import, U06's restricted target and F01's open broader duty are
sound. A few local qualifications would prevent a later implementer from
mistaking the comparison column for an instantiated theorem.

Observed input hashes:

- `01_problem_contract.md`: `2b278f1063e2169d412faf2cad93b6877ccaf41886252090bf2aa1fb1bc547f5`.
- `01_desiderata.md`: `b4f674b6dc157dda1d9da793001fa4daffc08a67ceed43b34b4fc3a91f8b9f17`.
- `li_desiderata_import_audit.md`: `727f02fb715bbe8d62a3132592ccbbeb499c080f93a3981a5ec2d1037d3af811`.

The principal reviewer may edit the canonical files concurrently; these hashes
identify the versions assessed, not a request to freeze them.

## Minimal concrete changes

**1. Add one import boundary after the matrix's introductory paragraph.**

> Cited theorems describe their own source systems under their stated
> hypotheses. This table does not instantiate those systems or transfer their
> guarantees to the candidate. A later claim must record the actual algorithm,
> encoding, information/feedback process and proof or reduction that licenses it.

This makes the present intent local to the matrix rather than dependent on a
reader following every linked source.

**2. U07: distinguish the two source conclusions in the disposition.**

Suggested addition:

> For LI comparisons, recurring calibration gives a limit-point statement;
> the selected feedback theorem gives convergence under additional conditions.
> Preserve the efficient Gamma-decidable family, weighting/divergence and
> deferral/timely-feedback hypotheses recorded in S01. A finite resolved-cohort
> statistic establishes neither asymptotic result.

Locators: [LI author PDF](https://intelligence.org/files/LogicalInduction.pdf),
Theorem 4.3.3; Definitions 4.3.5/4.3.7; Theorem 4.3.8; Appendices D.3/D.5.
The exact schemas are already in the import audit §4. This is a qualification
of a proposed target, not a correction to a claimed successful experiment.

**3. U08: name the output whose loss receives the bound.**

Suggested addition:

> Name the mixture/update rule and its scored output. If the output differs
> from the weighted allocation, supply the loss bridge; an unanalysed
> constraint projection does not inherit the bound.

Locator: [Freund–Schapire](https://cseweb.ucsd.edu/~yfreund/papers/adaboost.pdf),
§2 Figure 1, Theorem 2/Corollary 3. This matches the main contract §8's existing
composition warning. Bounded losses, full feedback and a finite expert set
alone do not specify a successful learning algorithm. In a convex score
setting, an appropriate mixture inequality can supply the bridge; arbitrary
postprocessing cannot be assumed to do so.

**4. U09: make the wrapper's base guarantee visible.**

Suggested addition:

> Record the base algorithm's regret assumptions and bound `f`, with
> `f(0)=0` and `f` nondecreasing and concave, as well as the applicable delay
> independence. Charge all active copies.

Locator: [Joulani–Gyorgy–Szepesvari](https://proceedings.mlr.press/v28/joulani13.pdf),
§3.1 Algorithm 1/Theorem 1. The current passive-versus-paid distinction is
correct. The added words prevent “exogenous delay” alone from being mistaken
for every hypothesis of the wrapper theorem.

**5. V01 / problem contract §6.1: identify the exact expectation bridge.**

Suggested addition after the finite-law sum:

> This exact finite expectation uses the supplied coherent law. LI's `E_n`
> is a threshold-price average with selected asymptotic coherence duties;
> its notation does not supply these exact finite identities. A deliberately
> constructed quote `v=1-p` is not automatically the market quote for
> `not phi`.

Locators: LI Definition 4.8.2; Theorems 4.8.4/4.8.6; audit §3. The current
equation is correct in its stated ordinary-model setting. This addition blocks
an unintended transfer from the theoretical LI comparison elsewhere.

## Rows that need no substantive status change

- **U05:** keep “later theorem target, not imported.” For precision, its source
  column can add “Gamma-relative; fixed-query and sequence quantifiers differ.”
  LI Theorems 4.1.1–4.1.2/4.2.1 do not grant correctness for every intended
  arithmetic truth. No assumption of Gamma's completeness or intended
  soundness should be inferred from its consistency.
- **U06:** keep “later restricted target.” A compact source-column qualifier
  would be “e.c. sequences of Gamma-theorems (respectively refutable
  sentences)” beside Theorem 4.2.1.
  An arbitrary recurring workload or a finite pre-resolution success rate is
  not that theorem's sequence-level statement.
- **F01:** keep “inherited bounded case; broader duty open.” Optionally append
  “Any later LI import must specify quotation/precision and the corrected
  source scope.” Locators: LI 4.11.1/Appendix F.1; pinned FAF PE6 and
  `Construction/Paper/Market.lean:452–477`. The inspected code-indexed endpoint
  and printed literal-numeral interface must not be silently identified.

These are clarifications of the existing dispositions, not reasons to mark
those duties failed or already achieved. No source-backed finite rate or
general reflection guarantee was established in this review.

## Correction to the earlier review's wording

In `li_desiderata_import_audit.md` §2, the empty-predicate paragraph currently
says “the displayed condition holds vacuously” immediately after displaying
the stronger admission formula. Replace those words with **“the weaker §2
condition holds vacuously.”** Only the weaker formula permits the empty
predicate. The stated counterexample and the intended existence distinction
remain correct; the antecedent of that sentence needs to be explicit.

Only this new review note was written. No canonical or earlier review file was
changed by this review, and no time was added to the principal ledger.
