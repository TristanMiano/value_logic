# Learning capped proof costs without inventing unresolved labels

Codex (GPT-6), s19 DEVELOPMENT. This is an ordinary bandit/portfolio
reduction and a comparator boundary, not a new generic learning theorem.

Let an action be a named proof procedure with a fixed finite work cap h.
On completion, its output must pass a sound checker. Otherwise a known,
valid fallback is used at charged cost F. Let R be work until a checked
completion, possibly infinite. The actual policy bill is

    min(R,h) + F*1{R>h},

with a stated convention at equality. The capped trace reveals this bill
exactly even when R itself remains right-censored. It does not label the
unresolved mathematical claim false or estimate the unobserved runtime tail.
A finite catalogue of such policies on fresh tasks therefore supplies ordinary
bounded bandit feedback, with checker, selection and fallback costs included.
No parametric survival model is necessary merely to learn these policy bills.
Different caps or uncapped-runtime objectives are different targets.

A longer trace of the same deterministic/random-seed-fixed procedure also
reveals the bills for all shorter caps. This is ordinary ordered side feedback;
it should be used as a stronger comparator to an implementation that treats
all timeout policies as unrelated arms. If an execution changes future state,
the next limitation applies.

## External regret can ignore a valuable proof cache

Two procedures each need m unit calls to complete a permanent certificate.
Before completion, a call costs1 and an immediate valid fallback costs1.
The completing call costs1; after completion its certificate answers every
future request at cost0. The two progress chains are disjoint and persistent.
Take T=2m-4 requests, m>=4. An alternating controller calls each procedure
m-2 times, never completing either, and pays2T.

At every actual visited state, either next procedure call still requires a
fallback, so both instantaneous losses are2. Its external regret against
those actual-state loss vectors is zero. A counterfactual controller that
always chose one procedure would pay2m-1 and then reuse its certificate,
giving actual policy regret

    2T-(2m-1)=T-3.

This is a counterexample to an inference from external to stateful policy
regret, not an impossibility theorem for all cache-aware algorithms. Progress
is monotone; no malicious deletion is needed. The missing comparison must
replay the comparator's own purchased proof state.

Ordinary round-robin portfolios give a different, explicit guarantee: if one
of K resumable procedures can finish a fixed proof in r own steps, the
portfolio reaches a checked completion within at most K*r steps, up to the
specified switching/checking bill. This does not imply near-optimal cumulative
cost on an arbitrary stream with shared facts. Keep the cache-state duty and
reject a generic new-principle claim for the capped-cost reduction.
