# Independent reconstruction: refinement and computed information

2026-10-07. Reviewer: **ChatGPT (GPT-6 Astra Pro)**, internal delegated reviewer. Read [criterion probes §4](../../../foundations/01_criterion_probes.md#4-refinement-has-several-non-equivalent-meanings) and [representation boundaries §2](../../../foundations/01_representation_boundaries.md#2-reading-a-program-is-not-the-same-as-cheaply-knowing-its-answer). P3-01 semantic/mathematical review only: no literature expansion, new algorithm, executable test or canonical edit.

**Disposition:** both arguments are correct within their stated conditional scope. The signal table does not establish that a bounded logical learner has the required probability model or can compute its conditional means. The new representation discussion explicitly preserves that distinction. One local condition should be added to the squared-loss purchase example: identify the allowed numerical report/action domain.

## 1. Reconstructing the four refinement services

For nonempty `W_new subset W_old` and the same real loss function, every value attained on `W_new` is also attained on `W_old`. Consequently the infimum can only increase and the supremum can only decrease. Extended extrema can be used if necessary. This is weak non-widening, not guaranteed strict narrowing. Soundness matters when the interval is claimed to cover the actual answer: subset inclusion alone says nothing about whether either set retained the true case. A loose certified enclosure can widen unless its construction also enforces nesting. The criterion note states these conditions correctly.

Expected predictive loss, realized predictive loss and paid decision loss have different quantifiers. Lower expected squared loss need not hold on every realized observation, and it need not reduce another action loss. Charging acquisition introduces a further objective. None of these implications can be recovered simply by calling all four improvements “refinement.”

## 2. Reconstructing the finite signal arithmetic

The three positive joint masses are `P(Y=0,S=0)=4/5`, `P(Y=0,S=1)=1/10`, and `P(Y=1,S=1)=1/10`. They sum to one. Thus:

| Quantity | Independent derivation |
| --- | --- |
| Prior mean | `P(Y=1)=1/10` |
| Signal probabilities | `P(S=0)=4/5`, `P(S=1)=1/5` |
| Conditional means | `p_0=0`, `p_1=(1/10)/(1/5)=1/2` |
| Prior squared risk | `(9/10)(1/10)^2+(1/10)(9/10)^2=9/100` |
| Conditional squared risk after signal | `(4/5)·0+(1/5)·(1/4)=1/20` |
| Expected improvement | `9/100−1/20=1/25` |
| Prior optimal Boolean-action error | `min(9/10,1/10)=1/10` |
| Post-signal optimal Boolean-action error | `(4/5)·0+(1/5)·(1/2)=1/10` |

On the positive-probability branch `(Y,S)=(0,1)`, the report changes from `1/10` to `1/2`, so its realized squared error increases from `1/100` to `1/4`. Conditional variance on `S=1` is likewise `1/4`, exceeding the prior variance `9/100`. These do not conflict with the lower ex ante risk.

**RI01 — local action-domain condition.** The `1/25` gross benefit applies when the decision permits the Bayes numerical report, for example actions `a in [0,1]` with loss `(Y−a)^2`. If actions are restricted to `{0,1}`, squared loss is exactly zero-one loss and the benefit is zero in this table. Suggested phrase: **“For a squared-loss report decision with actions in `[0,1]`, …”**. The purchase threshold is in the same loss units, for the stipulated single-use comparison with other materially different costs accounted for; it does not price future reuse automatically. The current “can be worth paying” wording appropriately avoids a universal recommendation.

## 3. Reconstructing the conditional decomposition

Write `p=E[Y|F]`, `p'=E[Y|G]` with `F subset G`, and `d=p'−p`. Bounded `Y` makes every term square-integrable. Expand

```
(Y−p)^2 = (Y−p')^2 + 2(Y−p')d + d^2.
```

The difference `d` is `G`-measurable. By conditioning first on `G`,

```
E[(Y−p')d | F]
  = E[d E[Y−p' | G] | F]
  = 0.
```

This yields the displayed equality, almost surely, and expected non-increase because `E[d^2|F]>=0`. Equality is possible. The argument uses conditional means under one probability law; replacing them by approximate learned reports requires an additional error analysis. Replacing the law, interpretation or filtration likewise does not inherit the equality automatically. No runtime assertion occurs in this proof.

## 4. Deterministic query families do not remove the computational gap

For a finite query index `Q` and a **Boolean-valued** fixed function `f`, the event `Q=q` fixes `Y=f(q)`. At every positive-mass query, `P(Y=1|Q=q)=f(q)` follows directly. Equivalently, the conditional variance given `Q` is zero. This is a statement about a mathematical joint law, not an algorithm for evaluating the conditional probability. “Boolean-valued” is a useful explicit type annotation for `f` in the displayed formula.

The signal table can be represented by three deterministic query cases with probabilities `4/5,1/10,1/10`, answer values `0,0,1`, and signal values `0,1,1`. Under that representation, its prior calculation uses the trivial information field and its posterior calculation uses `sigma(S)`. It does **not** use `sigma(Q)` as prior information. If `Q` were included in the full mathematical conditioning field, the conditional answer would already be degenerate and this acquisition could not deliver the claimed `1/25` information gain.

A procedure can nevertheless see the query string without having computed its answer. Its retained abstraction or stipulated epistemic model may therefore support a nondegenerate forecast. That forecast is not the ideal conditional probability given every mathematical consequence of the visible string. The new representation note says this expressly and permits ordinary competitors the same bounded methods and shortcuts. It supplies neither a particular abstraction's adequacy nor a general acquisition policy.

The large-table discussion is appropriately conditional on the access model. It should not be read as a lower-bound proof: finite determinism alone establishes no computational hardness, and a different encoding or charged advice can change lookup cost. The source text does not assert such a lower bound.

## 5. Scope and resource record

The reconstruction uses handwritten algebra and the stated finite table. No executable test was run, no prior test artifact was relabeled, and no general logical-uncertainty or learning guarantee was established. Only this review note was written. Own engaged duration, token usage and dollar cost are unmetered/unknown; **zero concurrent principal time credit**.

Reviewed working-file SHA256 values:

- `01_criterion_probes.md`: `d2e2cb3b6450d7bd7de993a357e184db73f364bfdeb16722683c864e0823a07e`
- `01_representation_boundaries.md`: `e1b6c6d465eac12b8f6fce364ebc540f8b3ea8649b19279e049838a995e03c92`
