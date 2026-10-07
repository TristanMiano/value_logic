# P3-03 frontier and retained-source probe — prospective plan

Contributor: **ChatGPT (GPT-6 Astra Pro)**, October 7, 2026 UTC.
Recorded before creating or executing the dedicated attempt. **DEVELOPMENT**;
no final freeze, challenge, gate, forecast-learning endpoint or extra concurrent
research credit.

The current source-refinement algorithm will remain unchanged. A separate
small evaluator will save its exact cases and source/code hashes before
importing that kernel and running each fresh numbered attempt.

1. On odd parity for `k = 2, 3, 6`, compare cell cap `C = 2^(k-1)` with
   `C+1`. At `C`, require an unchanged complete queue cycle of capacity stops,
   `C` one-free-bit cubes, and unresolved exact filtering. At `C+1`, require
   exactly the odd singleton assignments, parity loss range `[1,1]`, and the
   predicted counts: `2C-1` splits, `2C` singleton visits and `C(C-1)/2`
   capacity stops. Full odd-assignment tables are evaluator-only, never inputs.
2. For `k = 2, 4, 6`, use loss `min(x,1-x)` with no constraints. With the
   relevant coordinate last and cap `2^k`, its first zero upper bound should
   occur after `2^k-1` splits. With that coordinate first and cap two, one split
   should suffice. At these stopping points exact whole-source filtering and
   checked truth coordinates should still be unresolved. Record reporting and
   dispatch work separately; this is a scheduler comparison, not equal-cost
   recoding or a universal lower bound.
3. Exercise the two-bit withdrawal example in U03-10. The two original sources
   should both be `{11}` with loss `y=1`. Withdraw the same `h0: x=1` handle;
   verify the distinct revised sources `{01,11}` and `{00,11}` and respective
   loss ranges `[1,1]` and `[0,1]`. The original constraint records are distinct
   and remain the needed operational input.

Use one source transaction at a time with retained state. Detect a fixed-input
stall by a full unchanged queue cycle, not by elapsed timeout. An unexpected
50,000-transaction ceiling is a failed diagnostic, never proof of a stall.
Preserve complete small traces and any failed attempt. Once these named risks
are resolved, do not broaden the corpus or rerun the earlier general suites.
The hand proofs and same-model static review carry the general claims; this
probe checks the actual implementation's specified cases and accounting.
