# Option B: pre-run review of the complementary-domain family

Contributor: **ChatGPT (GPT-6 Astra Pro)**, integration reviewer, October 10,
2026 UTC. **DEVELOPMENT; same-model, nonblind independent reconstruction.**
Principal-clock credit: **zero**. Prospective mathematical/design review only:
no producer, checker, policy, timing or outcome runs. The proposed experiment
has not received a performance verdict.

## 1. Disposition

**The family is valid with an explicit rank-preservation condition.** Positive
rank weights and one free parity coordinate alone do not preserve the claimed
complementarity in the current incumbent sublevel. The strongest ordinary arm
should include **verified ADD bootstrap followed by the same portfolio kernel**.
That is a useful equal-service bridge, even if it removes a portfolio resource
advantage.

## 2. Domain proof and exact witnesses

Let $`n=k+2`$, with bits $`p,q`$ and parity coordinates $`z`$. Let $`A(z)`$ and
$`B(z)`$ be the forward and reverse XOR folds. Keep $`k\ge2`$ for distinct
expression syntax; in the old ten-bit fragment this permits $`2\le k\le8`$.
Define

```math
D=p-q+A-B=p-q,\qquad
L=\{p=0\},\qquad R=\{q=1\},
\qquad H=(\neg p\land A)\lor(q\land\neg A).
```

The old domains have no soft rows and cutoff zero. On $`L`$, $`D=-q\le0`$;
on $`R`$, $`D=p-1\le0`$. A complete assignment with $`p=0,q=1`$ is a feasible
incumbent for both old domains, for either parity.

If $`A=1`$, the current hard formula requires $`p=0`$. If $`A=0`$, it requires
$`q=1`$. Hence $`H\subseteq L\cup R`$ and the common zero bound is sound.
The useful witnesses are:

| Current point type | Parity needed | Old membership | Exact difference |
|---|---|---|---:|
| $`p=0,q=0`$ | $`A=1`$ | $`L\setminus R`$ | 0 |
| $`p=1,q=1`$ | $`A=0`$ | $`R\setminus L`$ | 0 |
| $`p=0,q=1`$ | Either | $`L\cap R`$ | -1 |
| $`p=1,q=0`$ | Neither is allowed by $`H`$ | Outside both | 1 |

Thus the hard domain is genuinely complementary and its loss is nonconstant.
For the actual service, each of the first three rows must survive the rank
cutoff and additional edit constraints, not just $`H`$.

## 3. Rank caveat and a robust edit contract

Counterexample to the underspecified rank condition: add positive-weight soft
formulas $`\neg p`$ and $`q`$. The proposed incumbent $`p=0,q=1`$ has rank zero.
Its sublevel retains only that pair. Both exclusive rows disappear, even if
all parity bits remain free. This invalidates complementarity and nonconstant
loss **for the requested receiving sublevel**, though the zero bound stays true.

A sufficient condition that also permits genuine rank filtering is:

- reserve one parity coordinate $`z_*`$ that occurs in both folds;
- make every additional hard restriction and every soft/rank formula depend
  only on $`z\setminus\{z_*\}`$, not on $`p,q,z_*`$;
- supply a complete admitted witness for those remaining coordinates with
  $`p=0,q=1`$, and derive the cutoff from that witness;
- preserve this condition across each declared edit.

Fix the witness's remaining coordinates. Their rank and additional hard truth
are unchanged by changing $`p,q,z_*`$. Flipping $`z_*`$ toggles parity, so both
exclusive points and the intersection point exist at the incumbent rank.
They therefore remain in the sublevel, including ties. Positive weights may
change and additional restrictions may change; each new witness must still
be admitted. Other coordinates may still be excluded by a genuine rank filter.
Record the three concrete witness assignments for every version before the
comparison. An exact mathematical proof of these witnesses is sufficient;
it does not require revealing a private evaluation population.

## 4. A small existing-kernel cover is already available

Assume both old zero-bound domains have been independently admitted, with
identity maps, scale one and unchanged difference syntax. The existing
portfolio receiver accepts this **five-node upper bound** on cover size:

1. Split $`p`$.
2. On $`p=0`$, reuse $`L`$.
3. On $`p=1`$, split $`q`$.
4. On $`p=1,q=0`$, exclude the cell because interval evaluation makes both
   disjuncts of $`H`$ exactly false.
5. On $`p=1,q=1`$, reuse $`R`$.

The mapped hard premise is established by the assigned bit, the old rank is
zero, and the loss correction is identically zero. This proof works regardless
of $`k`$ and any further current constraints/rank filtering. It is not claimed
minimal. Parity affects bootstrap or direct computation, but it does not force
the warm cover to split every parity coordinate. The separate full-cube parity
lower bound must not be transferred to this complementary-domain experiment.

## 5. Strong matched ordinary controls and domain admission

Include cold and owned-resident ordinary DAG receipt delivery; fresh tree
certification as an ablation; and the hybrid **ordinary checked ADD bootstrap
of both old domains, followed by exactly this portfolio receiver**. If exact
tables or a verified algebraic shortcut fit the declared receiving service,
retain them as credible ordinary methods. All methods may use the same kernel.
Disabling direct fallback is legitimate for a coverage diagnostic, but cannot
support the claim that a single old certificate prevents a stronger ordinary
method from answering through another route.

A safe new admission API should take raw ADD evidence plus the independently
supplied old frame, witness, bound, expected source/epoch and resident state.
It must run the independent checker, obtain the actually proved cutoff and
bound, then create the receiver-owned immutable `DomainCertificate`. An
untrusted status dictionary, root ID or digest is not admission authority.
Only success commits the fresh handle; failure leaves no partially admitted
domain. The old `PortfolioCache` permits admission only after verification;
preserve that property in a new adapter/version rather than directly exposing
its `_domains` dictionary or rewriting the old module.

The resulting domain certificate must bind the whole checked sublevel, exact
loss/unit, versioned old frame, cutoff and bound. The later portfolio checker
still reconstructs current feasibility, mapped old-premise coverage, old rank
containment and receiving loss correction. An old receipt remains a theorem
about its declared old domain; current applicability is proved separately.
Fresh receivers must replay the evidence chain, while a declared resident
receiver may retain verified state. Match that service choice across arms.

## 6. Cost and adversarial conditions to declare before the run

Charge both old receipt constructions, export/readout, independent checking,
portfolio admission and retained state before using the five-node cover.
Then charge each edit, current source validation, witness/cutoff computation,
proof generation/export, receiver checking and additional storage. Include
source setup and cap/failure work. Report direct and hybrid total bills over
the declared prefix; a final zero root or cheap last receipt is insufficient.

Useful prospective checks are narrowly tied to this contract:

- preserve the two exclusive and one intersection witnesses under every
  admitted edit; keep tied points at the cutoff;
- remove either old handle and demonstrate the uncovered exclusive point in
  the **reuse-only** route, while allowing ordinary fallback in the main arm;
- weaken $`H`$ to admit $`p=1,q=0`$: a stale zero-bound claim must not survive;
- change the loss, unit, source identity, order or epoch and reject an old
  mismatched raw receipt or prove a new claim through the proper path;
- reject a forged successful ADD report, an uncommitted receipt, a missing
  dependency, or an insufficiently funded admission without retaining a
  usable domain;
- include a constant/no-reuse control and count bootstrap even when no future
  request amortizes it.

This review establishes the mathematics and a fair control requirement. The
new wire implementation, resource caps and measured economics remain to be
reviewed after their source and prospective experiment contract are available.
