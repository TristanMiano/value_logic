# Accepted receiver reconstruction

Contributor/model: **ChatGPT (GPT-6 Astra Pro)**, 2026-10-10 UTC.
Independent same-model DEVELOPMENT reconstruction; zero principal-clock credit.
The selected task is [R-P3-B-B](../../selection.json), before P3-09.

## 1. The proposition to deliver

The existing portfolio receiver accepts a current finite Boolean frame, one
scalar positive-weight repair rank, a separately checked feasible incumbent,
one named receiving loss difference and its unit, and a proposed rational bound.
With incumbent $`z`$, its service concerns

```math
u=\rho(z),\qquad
Q_u=\{y:\mathrm{hard}(y)=1,\ \rho(y)\le u\}.
```

Acceptance proves that $`Q_u`$ is nonempty and that $`d(y)\le B`$ for every
$`y\in Q_u`$. In particular it covers every minimum-ranked repair, including
ties. It does not establish that the incumbent is optimal, identify every
minimizer, select an action separately in each hidden case, or produce an
online forecast. The receiving expression is fixed independently of the
producer. An unresolved external source needs its own covered request; it
cannot be made a repair variable and minimized away without a different model.

The ordinary ADD's old `query` computes the exact range on this same sublevel.
For equal certificate delivery it suffices to prove the Boolean function

```math
\mathrm{bad}(y)=\mathrm{hard}(y)
\mathbin{\wedge}[\rho(y)\le\rho(z)]
\mathbin{\wedge}[d(y)>B]
```

identically zero, while independently checking that the supplied incumbent is
feasible. The strict comparison against the bound and the non-strict rank
guard preserve equality and tied optima. A producer cannot choose a larger
bound or worse incumbent than the common service request supplies.

## 2. Actual proof checking and the trusted boundary

`05_counterfactual_transport.py` validates the exact current `Frame`: its
inherited immutable `Request`, full source/scope/interpretation metadata, the
named loss, the named unit, at most ten bits, and exactly one rank tier. A
frame comparison is a comparison of the full canonical record. A digest,
display label or proof name does not replace the independently supplied
record. This binds the formal input; it does not authenticate an empirical
interpretation or establish that the supplied physical model is adequate.

`verify_band` checks every split and both siblings of an old domain proof.
Each leaf is justified by a hard exclusion, a strict rank exclusion, or a
recomputed loss enclosure. The old band itself may be empty. The new
incumbent and mapped coverage prevent this from manufacturing a nonempty
current result.

`PortfolioCache.verify` independently derives the current cutoff and current
conditional inequality premises. It checks every reuse leaf's mapped old
hard constraints, old rank threshold, positive loss scale and receiving loss
correction. Negative multipliers on one-sided inequalities are forbidden;
equality consequences are represented with both signs. It checks the whole
current cover. A direct leaf is fresh current reasoning and is labelled as
such. A proof with no old choices is permitted. An empty or partial tree is
not a complete cover, and a rejected cover is not a proof that a comparison
is false or that a particular uncovered point is an optimum.

The portfolio's private cache contains only domains admitted by those proof
checks. It is trusted process state. A saved domain summary cannot be loaded
as authority in a fresh receiver; the old proof and any required chain must
be read and checked again, or an explicitly persistent receiver must retain
the admission. Handles are fresh and refer only to previous admissions, so
the supported admission history is acyclic. The implementation provides no
hostile-memory sandbox, cryptographic authentication or general native-v2
proof compiler.

`05_verify_evidence.py` has a different purpose: it checks archived filenames,
hashes and agreement between saved manifests/results/summaries. It expressly
does not replay a mathematical proof or an execution. Its PASS must not be
used as the new receiving certificate check.

The ordinary ADD manager also currently trusts its private tables. Its node
export is audit data, not an independently admitted proof. A small root alone
does not prove that it denotes the requested expression. The new receiver
must establish node meanings, pointwise Apply claims and expression bindings,
then reconstruct the current guard and bad function from those meanings.
Only unconditional expression denotations may survive an edit. A relation
true under yesterday's hard guard cannot be cached as an unconditional fact.

## 3. A precise legacy tree expansion witness

For at least two coordinates, take no hard or soft constraints and let the
fixed difference be forward-associated parity minus reverse-associated
parity, as constructed by `05_resource_comparison_check.py`. Both functions
are equal. In the old enclosure language their differently ordered syntax
produces distinct nonlinear atoms. On every Boolean cell with a free bit,
each parity interval is still $`[0,1]`$, so the difference enclosure has upper
bound one. The requested bound is zero. Hard and strict-rank exclusions are
unavailable, since the rank is identically zero.

Consequently `build_band` needs singleton leaves for this fixed input and
these fixed leaf rules: $`2^n`$ leaves and $`2^{n+1}-1`$ total nodes. The
empty-library portfolio's direct rule has the same obstruction. Its current
context contributes the zero rank row and equalities for already fixed bits;
these do not identify the two opaque parity features. Those equalities are
exactly zero on the cell, and cannot reduce the remaining parity interval.
There is no reuse choice in this claim.

A reduced ordered ADD represents the common parity function with shared
subgraphs, and subtraction of the identical roots yields terminal zero.
A checked DAG can preserve those unconditional denotations. This is a
statement about this representation and these local legacy proof rules. It
is not a lower bound for every portfolio, for a portfolio already containing
a useful admitted lemma, for an alternative proof system, or for ordinary
methods allowed to share a valid certificate procedure. The published
implementation is finite with at most ten bits; asymptotic language describes
the family only if that external cap is lifted. The complete old setup and
every new export/check must still be priced.

## 4. Edits, complementarity and boundary cases

The accepted complementary-domain case fixes current hard constraints
$`p=q`$ and $`r=1`$. Old domains have $`p=q=r=0`$ and $`p=q=1,r=0`$.
Mapping old coordinates to $`(p,q,0)`$ lets their union cover the current
source even though no literal old state survives. Both certify the same
receiving difference, $`\max(p-q,q-p)-1`$, with bound minus one. This is
genuine joint coverage with one action. A strong ordinary method may simplify
the same current expression using the equality, so it supplies no generic
resource advantage.

The following cases belong in the new finite contract and focused checks:

| Boundary | Required disposition |
|---|---|
| Tied ranks and a bound attained exactly | Keep the whole non-strict sublevel; accept loss equality. |
| Infeasible incumbent or genuinely empty current hard set | Reject this nonempty service, even if the bad root is zero. |
| Empty old band or no old choices | Empty old bands supply no uncovered current cases; no choices can still use a valid direct proof. |
| Missing sibling, unknown old handle or wrong old record | Reject the proof; do not infer falsity of the receiving claim. |
| Changed loss, unit, scope, metadata type or source version | Rebind the independent current record and recheck the claim; never accept a stale advertised report. |
| Repriced weights or withdrawn hard constraints | Rebuild the current rank and hard guard; unconditional ADD denotations alone may remain cached. |
| Opposite actions selected in separate hidden cases | Do not combine them into a guarantee for one unobserving action. |
| Malformed wire, duplicate keys, invalid rational, cycle, forward reference or missing Apply premise | Reject before state admission; preserve spent work in the common wrapper. |
| Stale epoch/order/source or wrong resident base counts | Reject; a wire message cannot authorize reset or reuse another receiver's cache. |
| Resource denial during input, construction, export or checking | No success certificate; the common wrapper must return the paid failure prefix and protected terminal receipt. |

The inherited `Request` admits zero bits, but the ordinary ADD manager admits
one through ten. The initial common scope should say one through ten rather
than silently promising a zero-coordinate implementation. Inherited input
rationals have at most 128 bits per component; intermediate ADD terminals
have a separate cap. The new wire cap must be explicit and equally applied.

## 5. Resource and comparison interpretation

The old raw counters cover selected operations, not every setup, arithmetic,
source read, serialization, memory operation or failure prefix. They are
useful diagnostics and cannot be renamed a complete uniform resource bill.
The new parent-owned wrapper supplies the declared event and byte tariff,
including setup, independent current/source admission, construction, every
edit, wire production and transfer, checking, retained storage and terminal
success/failure output. Receiver-state commits must occur only after a whole
claim succeeds, and protected terminal funding must survive a denied stage.

The strongest ordinary comparator may retain a verified DAG and send deltas,
or use the same portfolio algorithm. A cold receiver requires full evidence
and previous required admissions. A resident receiver may reuse its own paid,
verified unconditional state. These are separate service modes. Requiring
ordinary output to expand into a tree while permitting the candidate a
shared proof cache would make a format-specific comparison, not an equal
general receiving service. Conversely, retained proof state and larger source
closure have real setup/storage costs even when a later delta is tiny.

No new policy run or final evaluation supports this reconstruction. The source
manifest in this folder identifies the exact accepted code and derivations
read; old files are preserved.
