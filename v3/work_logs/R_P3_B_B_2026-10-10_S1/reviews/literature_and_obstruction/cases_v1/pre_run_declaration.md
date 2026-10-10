# Prospectively fixed certificate-delivery cases, version 1

Contributor: ChatGPT (GPT-6 Astra Pro), integration reviewer and fixture author, 2026-10-10 UTC. Same-model, nonblind DEVELOPMENT preparation for R-P3-B-B. Zero overlapping principal research-time credit.

## Fixed inputs and execution boundary

The [exact declaration](fixture_declaration.json) fixes four streams, six current requests per stream, and five old bootstrap requests in total. The [preparation binding](preparation_binding.json) records the exact source closure, serialization hash, and shared module identities. Construction and serialization succeeded. No scalar truth reference, ADD producer, independent evidence receiver, portfolio policy, or scientific benchmark was executed in this preparation.

The fixture module is [05_certificate_delivery_cases.py](../../../../../checks/05_certificate_delivery_cases.py), version `rp3bb-certificate-cases-v1`, SHA-256 `adfcaf7733b6b401033a7689815c277f746f8fcfe47c1ec7e1733ae8142ca163` (18,685 bytes). The immutable captured copy is [here](source/v3/checks/05_certificate_delivery_cases.py). The declaration SHA-256 is `2ec5e0663ace94c511f299aec2ec3a506f8889c799e79378d01c7bbf52144c87` (224,731 bytes). The baseline is `33c6d6795aac894bd3cf8575e44f1d6f38f6ae56`.

| Fixed stream | Boolean bits | Variable order | Old requests | Current requests | Requested bounds |
| --- | ---: | --- | ---: | ---: | --- |
| `constant_n3` | 3 | 0, 1, 2 | 0 | 6 | minus one throughout |
| `parity_reassociation_n6` | 6 | 0 through 5 | 1, full cube | 6 | zero throughout |
| `complementary_k3_n5` | 5 | 0 through 4 | 2, left and right domains | 6 | zero for edits 0–4; one half for edit 5 |
| `complementary_k5_n7` | 7 | 0 through 6 | 2, left and right domains | 6 | zero for edits 0–4; one half for edit 5 |

Every record fixes the full inherited `Frame.record()`, declared loss unit, versioned source scope, witness, and exact rational bound. Old handles have distinct names and fixed index order: `left_not_p` then `right_q` for the complementary streams. The constant control intentionally has no bootstrap certificates. The stream supplies the explicit identity replacement map for every old-to-current comparison; dimensions and coordinate meanings are fixed within each stream.

## Exact family definitions

In the constant stream, the difference is the literal minus one. The six hard/rank settings are, in order: no rows; hard not-bit-0 with preference for bit 1 of weight 1; hard bit 0 with preference for bit 1 of weight 2; hard not-bit-2 with preference for not-bit-1 of weight one half; hard equality of bits 0 and 1 with preference for bit 2 of weight 3; and hard bit-0-or-bit-2 with preference for not-bit-1 of weight 2. The complete witnesses are fixed in the JSON. These requests expose constant/no-reuse overhead under the same receiving service.

The parity stream uses the six-coordinate forward and reverse XOR folds. If they are denoted by $`P`$ and $`Q`$, the difference is $`P-Q`$. The old domain is the full cube with rank zero. Every current request keeps bit 5 absent from extra hard/rank rows. Edits 0–5 respectively use: no extra hard row with preference for bit 0; hard not-bit-0 with preference for bit 1; hard bit 0 with preference for not-bit-1; hard equality of bits 0 and 1 with preference for bit 2; hard bit-2-or-bit-3 with preference for not-bit-4; and hard not-bit-0 with preferences for bit 1 and not-bit-2. Weights and witnesses are fixed exactly in the declaration.

For either complementary stream, bits 0 and 1 are $`p,q`$. The remaining $`k`$ bits are the parity coordinates. Let $`A`$ be their forward XOR fold and $`B`$ their reverse fold. The old domains and shared difference are

```math
L=\{p=0\},\qquad R=\{q=1\},\qquad D=p-q+A-B=p-q.
```

Both old domains have no rank rows, incumbent rank zero, bound zero, and the declared incumbent $`p=0,q=1`$ with all parity coordinates zero. The common current hard formula is

```math
H=(\neg p\mathbin{\wedge}A)\mathbin{\vee}(q\mathbin{\wedge}\neg A).
```

The last parity coordinate $`z_*`$ is protected: bit 4 in `complementary_k3_n5`, bit 6 in `complementary_k5_n7`. Every additional hard formula and every soft rank formula uses only the other parity coordinates. For edit index $`j`$, let $`u`$ and $`v`$ be the cyclic consecutive coordinates selected by the source's `other[j % len(other)]` rule. The exact additions are:

| Edit | Extra hard formulas | Soft formulas and positive weights | Fixed incumbent values of $`u,v`$ | Difference and bound |
| --- | --- | --- | --- | --- |
| 0 | none | prefer $`u`$, weight 1 | 0, 0 | $`D`$, 0 |
| 1 | $`\neg u`$ | prefer $`v`$, weight 2 | 0, 0 | $`D`$, 0 |
| 2 | $`u`$ | prefer $`\neg v`$, weight $`1/2`$ | 1, 0 | $`D`$, 0 |
| 3 | $`u=v`$ | prefer $`u`$, weight 1; prefer $`\neg v`$, weight 2 | 0, 0 | $`D`$, 0 |
| 4 | $`u\vee v`$ | prefer $`\neg u`$, weight $`3/2`$; prefer $`v`$, weight $`1/2`$ | 1, 0 | $`D`$, 0 |
| 5 | $`\neg u`$ and $`v`$ | prefer $`u`$, weight 2; prefer $`\neg v`$, weight 1 | 0, 1 | $`D+1/2`$, $`1/2`$ |

All other incumbent parity coordinates are zero; $`p=0,q=1`$. Each soft formula contributes its positive weight exactly when false, in the single declared rank tier.

## Why complementarity survives all six edits

The proof is syntactic and algebraic; the exhaustive reference has not yet been run. Fix the other parity coordinates to the declared incumbent values. Adjusting only $`z_*`$ can make $`A`$ either zero or one without changing any additional hard formula or rank row. Thus the two declared exclusive witnesses are $`p=0,q=0,A=1`$ and $`p=1,q=1,A=0`$. Both satisfy the complete current hard domain and have the same rank as the feasible incumbent. Their inclusion therefore survives every edit and the incumbent-sublevel cutoff, including ties. The incumbent $`p=0,q=1`$ remains in the intersection.

Consequently, neither old domain alone covers the current incumbent sublevel, while their union does. The difference takes both $`-1`$ and $`0`$ there; in the last edit it takes both $`-1/2`$ and $`1/2`$. The last edit requires the explicit half-unit drift allowance when importing the old zero bounds. These are conclusions for this declared family, with the protected-coordinate condition enforced by construction.

As the [pre-run mathematical review](../pre_run_design_review.md) explains, once both old domains have been independently admitted, the existing portfolio leaf rules permit a five-node coverage tree: split on $`p`$; reuse the left domain on $`p=0`$; split the other branch on $`q`$; exclude $`p=1,q=0`$ using the current hard formula; reuse the right domain on $`p=1,q=1`$. This is an upper bound for this reuse route, not a minimality claim. The empty-cache parity tree obstruction must not be promoted to a lower bound against this admitted portfolio or against shared DAG evidence.

## Reference and receiving interfaces

`streams()` returns immutable `Stream` records with `.name`, `.nbits`, `.order`, `.old`, `.edits`, `.protected_free_bit`, and `.identity_replacements`. Each `Case` exposes `.frame`, `.witness`, `.bound`, `.name`, and the distinct `.handle`. `record()` supplies exact JSON-compatible contents. The fixtures share the already admitted `_p305_portfolio_base` and `_p305_inherited_p304` module objects with producer and receiver code, avoiding incompatible copies of the inherited classes.

`scalar_value(expression, point)` and `scalar_report(frame, witness, bound, expected_current_record=...)` directly implement the finite grammar's scalar semantics. They use the inherited parser/admission checks, but no interval enclosure, ADD, portfolio, rank helper, or certificate acceptance to compute truth. `reference_report(case)` binds the current record automatically. A feasible incumbent gives `NONEMPTY`; the result states the requested bound and the entire current incumbent-sublevel coverage, including all minimizers. A false bound returns its first actual counterexample. The exact lower/upper values, hard/sublevel sizes and minimizer counts are explicitly diagnostic fields.

The scalar reference output is not portable proof authority. Named exclusive witnesses are public development diagnostics; the runner must not silently give them to a policy as an uncharged oracle. A deployed exact-table arm may use the reference only with its source and computation charged. This preparation assigns no cost tariff and makes no speed, storage, export, editing, checking or budget result. Root owns the common receiving service and tariff and will freeze the full executing source closure before measurement.

## Reproduction and scope

The preparation command was `python v3/work_logs/R_P3_B_B_2026-10-10_S1/reviews/literature_and_obstruction/prepare_cases_declaration.py`, from the repository root. It refuses to overwrite its `cases_v1` output directory. For independent reconstruction, restore the captured fixture and its two inherited dependencies at their original relative paths, then call `declaration()` and serialize with sorted keys, two-space indentation and a final newline. The captured preparation script records the exact procedure and does not call the scalar reference.

These are four public, deliberately structured development streams. They do not establish performance on held-out inputs, a general certificate lower bound, general runtime tractability, or final evaluation. No scientific or principal clock claim is made by this artifact.
