# Compulsory calibration cannot establish source adequacy

**DEVELOPMENT — Codex (GPT-6), October 14, 2026 UTC.**
This is a constructive limit and a priced diagnostic repair, not a rejection
of the in-family compulsory-pair theorem.

Use the three-vertex path 0–1–2, with audit fees (2,7,2). Indicators are E
(extreme) or M (middle); conditional extreme labels 0/2 may be drawn with
the same independent fair rule in both laws and do not affect the argument.
Let P be independent fair indicators, the admitted Markov source rho=1/2.
Define a different fresh-row law Q:

- With probability 1/2 the center is E and both endpoints are M.
- With probability 1/2 the center is M and its endpoints are independent fair
  E/M indicators.

The center-first exact policy audits node 1. On E it stops; on M it must
audit both endpoints. Its entire receipt-history law is **identical under
P and Q**: the center has the same fair indicator, and the fully observed
middle-center branch has the same conditional endpoint distribution. This
remains true over every number of fresh requests. In particular, its
compulsory first-middle/next-neighbor samples are iid Bernoulli(1/2) under
both laws. No statistical procedure using only these center-policy receipts
can distinguish the two sources, however many receipts it collects.

But the ranking of two exact acquisition policies reverses. Center-first
has expected fee 7+(1/2)(2+2)=9 under both laws. The leaves-first policy
queries endpoint 0, then follows the standard exact star rule: a middle
endpoint forces the center; if the center is middle, query the other endpoint;
an extreme first endpoint instead leads to endpoint 2, whose middle value
then forces the center. Its expected fee is

```math
V_{\mathrm{leaf}}(P)=35/4=8.75<9,
\qquad V_{\mathrm{leaf}}(Q)=73/8=9.125>9.
```

Therefore a source-model fee certificate learned from these compulsory
receipts has no distribution-free warrant for the unexecuted policy ranking.
The parameter confidence statement is sound **conditional on the source
family**. A very small parameter interval does not establish that premise.
This does not prove that every adaptive controller is unable to learn: a
different policy can expose new information. It identifies the missing
observation under the particular deployed acquisition policy.

## A small, explicitly paid adequacy probe

When center-first observes E, select a diagnostic request with independently
chosen probability eta>0 and buy endpoint 0 as one **additional** audit.
Conditional on this context, endpoint M has probability 1/2 under P and one
under Q. This contrasts with the compulsory middle-center samples, whose
law is unchanged. The source discrepancy is located in a context where the
action was already certifiable and its otherwise unnecessary receipt was
missing.

For the simple P-versus-Q diagnostic, multiply an e-value by two for each
pilot M and by zero for a pilot E. Under P this is a nonnegative martingale.
At a threshold of 20, five all-M pilot samples reject P with probability at
most 1/20; under Q they arrive after an expected 10/eta service requests and
cost ten additional audit-fee units. The exact type-I probability for the
first-five rule is 1/32. This test does not verify P when it fails to reject,
nor establish that Q exhausts all alternatives.

The example suggests **decision-relevant adequacy probes**: identify source
assumptions needed to rank otherwise exact policies, find observational
contexts where competing source laws disagree, and price a small probe there.
This is related to ordinary identifiability, active testing and partial
monitoring. Its usefulness must be measured against those constructions with
the same probe access. Exact logical action safety and uncertain expected
acquisition efficiency are distinct guarantees throughout.
