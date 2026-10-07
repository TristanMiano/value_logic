# P3-01: finite perturbation source scope

Reviewer: **GPT-6 Astra Pro**, `/root/p301_induction_sources`.
Date: **2026-10-07 UTC**. Same-model internal, nonblind source/import review.
Scope: inspect one load-bearing LI import; reconstruct the restricted argument
needed by P3-01. No canonical edits, later-task execution, Lean build,
publication or novelty credit.

**Disposition:** the distinction raised by the principal reviewer is real.
The inspected primary definitions do not restrict early pricings to finite
belief states. A primary formalization project already records the unrestricted
statement's refutation and a corrected theorem for finitely many changed
`(day, sentence)` quotes. The one-quote witness in
[li_information_boundary.md](li_information_boundary.md) remains valid by the
direct restricted proof below. Its broad import of Theorem 4.6.1 should be read
with this correction; it is unnecessary for that witness.

## 1. Primary source contracts and exact inspection scope

### Original LI paper

Source: [Logical Induction](https://intelligence.org/files/LogicalInduction.pdf).
Definitions 3.1.2–5 (printed pp. 14–15) distinguish general computable rational
markets from finite-support belief states. The §4 standing assumptions
(p. 22) explicitly choose the general class. Appendix A.2 (pp. 79–81)
permits price features for any sentence at any past day. Appendix G.7
(pp. 126–127, especially PDF extraction lines 9541–55) replaces early
price features by constants and invokes finite hard-coding to justify
efficiency. Theorem 4.6.1 itself is on p. 36.

### Existing primary correction

Project: **A. M. Berns, Formalized Agent Foundations**. The principal reviewer
pinned commit `367d1e42bf104706ff28d8a40492b9ce95c98da0`, tree
`397e61e644547031ee90b58a20849358ed4b48df`, observed 2026-10-07 01:26:15 UTC.
This reviewer fetched the three code files at that immutable commit.

| Primary locator at the pin | Inspected contract |
|---|---|
| [FinitePerturbations.lean](https://github.com/A-M-Berns/Formalized-Agent-Foundations/blob/367d1e42bf104706ff28d8a40492b9ce95c98da0/LogicalInduction/Properties/FinitePerturbations.lean), definition `FiniteSupportPerturbation`, lines 439–440 | A finite set of `(day,sentence)` coordinates contains every difference. |
| [Oracle.lean](https://github.com/A-M-Berns/Formalized-Agent-Foundations/blob/367d1e42bf104706ff28d8a40492b9ce95c98da0/LogicalInduction/Construction/Freeze/Oracle.lean), `FreezeOracle.lic_iff_of_finiteSupport`, lines 620–627 | Two computable markets with finite coordinate differences satisfy LI equivalently, for the same process. No caller patch certificate or sentence restriction remains in this signature. |
| [Counterexample.lean](https://github.com/A-M-Berns/Formalized-Agent-Foundations/blob/367d1e42bf104706ff28d8a40492b9ce95c98da0/LogicalInduction/Construction/Freeze/Counterexample.lean), `not_overgeneral_ifp`, lines 771–775 | The declared closed result negates unrestricted eventual-day-agreement preservation. Its theory-parametric route uses a consistent delta-one theory extending `I-Sigma-1`; the closed endpoint instantiates that theory. |
| [paper-errata.md](https://github.com/A-M-Berns/Formalized-Agent-Foundations/blob/367d1e42bf104706ff28d8a40492b9ce95c98da0/LogicalInduction/notes/paper-errata.md), PE1 | Prior correction lead and counterexample explanation: one early pricing can supply historical sign/schedule advice indefinitely. |

The code declarations were inspected, not independently built or kernel-audited.
The repository's own formal-verification claims must retain that attribution.
The September 2026 Berns/Taylor discussion led to the repository; no secondary
newsletter is needed as mathematical authority. This is established prior work,
not a discovery claimed for P3-01.

## 2. Our diagnosis of the original efficiency inference

Finitely many day indices do not bound the number of sentences that later
traders can mention at those indices. For an efficiently emitted sequence of
distinct sentences `phi_n`, the coefficient `price(phi_n, day 1)` is a legal
rank-one feature on every day `n`. Its union of historical quote queries is
infinite, despite each individual output being finite.

Therefore replacing every old-day leaf by its exact original value need not
be a lookup in one finite table. Hard-coding a computable pricing program is
different from hard-coding its answers. Running that program on new sentence
inputs has no polynomial bound from mere computability; exact rational output
serialization has no such bound either. Nothing in the inspected expression
syntax changes a general computable function into an efficient primitive.

This argument identifies the unsupported inference in the displayed proof.
It alone would not prove the theorem false. The existing primary correction
supplies a separate refutation construction. We have inspected that project's
endpoint statements and its mechanism, without independently auditing the full
diagonal/settlement/compiler dependency chain.

There are sufficient additional assumptions under which an efficient replay
argument does work: finite changed quote coordinates; finite-support early
belief states on both sides; or uniform polynomial-time exact evaluation and
serialization of the old pricing functions on the needed inputs. The second
implies the first when only finitely many days change. The third is a real
extra assumption, not the original definition of a market. For a particular
trader, a fixed finite set of queried early coordinates also suffices; the
original universal trader quantifier provides no such restriction.

## 3. Direct finite-coordinate proof for our actual witness

This is an independent reconstruction of the known restricted argument, not
a new theorem claim. Let `P` and `Q` be computable rational markets assessed
against the same deductive process `D`. Suppose they differ only within a
fixed finite set

```math
K\subseteq\mathbb N_{>0}\times S.
```

Let `T` be an efficient trader against `P`, with coefficients `a_(n,phi)`.
Transform its coefficient expressions as follows: replace a price feature
`price(psi,i)` by the rational constant `P_i(psi)` precisely when `(i,psi)`
lies in `K`; leave every other price feature unchanged. Call this transform
`F_K`.

There are only finitely many changed coordinates and finitely many constant
values to insert. Under the paper's literal sentence/expression interface,
comparison with this fixed finite set and syntactic substitution have
polynomial cost in the input expression size. The constants have fixed finite
encodings. Rank and continuity are preserved. Thus transforming the output of
an efficient trader still gives an efficiently generated coefficient sequence.

For every original coefficient `a`, structural induction on its expression
gives

```math
F_K(a)(Q)=a(P).
```

Define the new trader to buy the same sentence quantities using these
transformed coefficients, but at the actual current prices of `Q`. Its share
positions equal those of the original trader on every day. Its cash payments
can differ only at coordinates in `K`. Hence the difference in cumulative
wealth at time `n`, for any assessment world `W`, is

```math
W(H^Q_n)-W(H^P_n)
=\sum_{\substack{(i,\phi)\in K\\i\le n}}
a_{i,\phi}(P)\bigl(P_i(\phi)-Q_i(\phi)\bigr).
```

Its absolute value is at most the finite constant

```math
C=\sum_{(i,\phi)\in K}
\left|a_{i,\phi}(P)\bigl(P_i(\phi)-Q_i(\phi)\bigr)\right|.
```

This bound is uniform in world and time. A common lower bound and an
unbounded set of upper wealth assessments survive a uniformly bounded
perturbation. An exploiter of `P` therefore yields an exploiter of `Q`.
Exchange `P` and `Q` to obtain the reverse direction. This proves the
restricted preservation claim for the needed interface.

### Application to the P3-01 separator

Choose a consistent process with `theta` in `D_1` and an existing logical
inductor `P`. Assign `Q_1(theta)=1/2`, leaving every other dated quote alone.
The difference set is contained in `{(1,theta)}`, so the proof just given
preserves LI. Yet every current assessment world satisfies `theta`, whereas
its first-day quote is one-half. Thus LI does not require exact finite-day
hard-evidence coherence. The application uses one coordinate and needs no
unrestricted whole-day perturbation theorem.

## 4. Source-version and reporting qualifications

The initially fetched moving-branch erratum text contains two stale-scope
warnings: its final suggested wording still mentions a residual syntactic
condition, and its theory-parametric description mentions Sigma-one
soundness. At the pinned code inspected here, the corrected public endpoint
has no such sentence condition; `Counterexample.lean` line 69 assumes
delta-one definability, inclusion of `I-Sigma-1`, and consistency. Its module
comment explicitly states that soundness is not assumed. Use the actual
pinned declarations, not those stale paraphrases. The principal reviewer is
preserving the source snapshot and reviewing the pinned erratum prose.

No stronger conclusion is needed for P3-01. In particular, this note does not
certify the whole formalization, transfer every amended LI property into the
finite project, or assign novelty to the historical-advice observation.

## 5. Resource observation

Raw start: `2026-10-07T01:23:19.248015+00:00`,
`time.monotonic_ns() = 29368555162096`.
The completion observation records elapsed span only. Tool waits and
orchestration gaps are included; this is not an audited engaged-work
measurement and adds **no principal ledger credit**.

Raw completion: `2026-10-07T01:28:41.835268+00:00`,
`time.monotonic_ns() = 29691142410348`.
Observed elapsed span: `322.587248252` seconds; no principal credit.
