# Shared proof progress as an online covering resource

Codex (GPT-6), October26,2026. DEVELOPMENT; proposed bounded adapter.

## Explicit contract

There are m resumable deterministic proof procedures. Procedure j produces a
checked reusable certificate after R_j units of charged work, with R_j
unknown and possibly infinite. Work includes verification and progress is
preserved without switching cost in the initial divisible-work model.
Request t has a known fallback price c_t>=0 and a known set I_t of certificate
types that would discharge it. Once any such certificate is checked and
stored, the request is discharged at zero additional modeled cost. Validity
and applicability are warranted independently of a fallible prediction.
The source and certificate meanings do not change during the sequence.

This is a restricted persistent-proof service, not arbitrary theorem proving
or arbitrary changing-source reuse. It excludes free fallback-generated
certificates, unknown applicability, uncharged state transfer and latency
constraints. Any practical adapter must account for these explicitly.

## Search implements a primal-dual process

If a stored certificate covers request t, answer it immediately. Otherwise
set y_t=0. Increase y_t continuously while running every unfinished j in I_t
at one unit of procedure work per unit increase. Stop at the first checked
covering certificate, or at y_t=c_t. In the latter case, if no certificate
has arrived, pay the fallback. A single physical processor can emulate the
fluid schedule; total charged work per increment is |I_t| times the increment.

Let d=max_t|I_t|. For every j, its accumulated work is

    p_j=sum_(t: j in I_t) y_t <= R_j.                    (S1)

After completion, later requests containing j are already covered and
receive y_t=0. Before completion the work cannot exceed its completion
threshold. A request's y_t never exceeds c_t. These are exactly feasible
dual variables for the fractional prize-collecting set-cover relaxation

    min sum_j R_j*z_j + sum_t c_t*r_t
    subject to sum_(j in I_t) z_j+r_t>=1, z,r>=0.

Infinite R_j simply excludes that purchase. Weak duality gives sum_t y_t
at most the offline cost of any actual proof/fallback cover. Total search
work, INCLUDING every unfinished procedure, is at most d*sum_t y_t.
Fallback is paid only at y_t=c_t, so its total is at most sum_t y_t. Hence

    total online cost <= (d+1)*OPT.                     (S2)

Here OPT may know every R_j and the whole finite request sequence, and may
choose any subset of reusable certificates plus individual fallbacks. It
still pays for their proofs. This is a genuine stateful comparator; unlike
instantaneous external regret it values a certificate's future reuse.
If no procedure ever finishes, (S2) remains meaningful through fallback.

The proof is ordinary online primal-dual covering. Its prospective content
is an explicit unknown-proof-cost interface where unfinished search work
also satisfies the charge bound. Known-cost online set cover does not by
itself charge simulation of every nonselected proof. No novelty, tightness,
bit-complexity or implemented runtime claim is yet made.

## Elementary tradeoff and failure boundaries

On a single repeated duty with K applicable procedures, d=K and this
recovers the K+1 bound from proof_investment with alpha=K. If applicability
is sparse, d can be much smaller than the total library size m. Choosing a
single predicted proof and never testing alternatives has no such worst-case
guarantee: the predicted procedure may never finish while another costs1.
The identical ordinary covering scheduler ties(S2).

If a certificate expires or an edit invalidates it, the argument that all
later covered requests have y_t=0 fails. Repeatedly charging the same finite
R_j constraint would violate dual feasibility. Restarting per certified
epoch gives a sum of epoch bounds against an epoch-wise comparator, not
against an offline policy that transports certificates cheaply across edits.
This is a concrete boundary on how counterfactual reuse can enter the model.

Next screen: unknown-cost/nonclairvoyant online covering and paid search.
If this interface is already treated directly, retain it as an ordinary
control rather than launch a proof or benchmark campaign.

## Closest early screen

Azar--Chiplunkar--Kutten--Touitou2020, section6, already gives the same
frequency-plus-one factor by counters and dual fitting for set cover with
delay (Theorem14, Lemmas15--17). Its sets have known buying prices and a
purchase covers currently pending requests, not all later arrivals. Here
prices are unknown proof completion times, unsuccessful progress is paid,
and certificates persist. The charging architecture is inherited almost
verbatim. This prevents claiming a new competitive-analysis principle.
Whether the hidden-work implementation is a useful moderately novel adapter
remains open; absence of a matching search result is not novelty evidence.

Ordinary known-price covering algorithms and this exact progress scheduler
must both be controls. The former's foreknowledge of R_j is a stronger
information contract, while the latter ties our behavior and bound.

## Discrete proof instructions without a per-request rounding loss

Suppose proof work is resumable in unit-cost instructions and finite R_j
are positive integers. Fallback prices may still be arbitrary nonnegative
rationals. Maintain a rational virtual credit z_j for every procedure.
Increasing y_t increases each applicable z_j by the same amount. Whenever
z_j reaches its next integer, execute the corresponding next instruction.
Stop at certificate completion or the request's fallback cap. At simultaneous
integer crossings, finish all instructions due at that crossing before
returning. Thus physical work is floor(z_j), with no ceiling of each small
request's budget. A tiny request can leave a fractional credit for later use.

For an unfinished procedure, z_j<R_j: otherwise the integer crossing at R_j
would already have produced its certificate. For a finished procedure,
z_j=R_j and every later applicable request is covered. Hence the same dual
constraints hold, while actual instruction cost is at most sum_j z_j.
The factor d+1 survives for this discrete instruction model. A procedure
with no proof can run forever across an infinite stream but receives only
bounded work on any finite paid prefix. A known zero-cost certificate is
initially installed rather than treated as an unexecuted positive-length run.

This counts proof instructions and fallback tariffs, not every instruction
of the controller. Enumerating applicability, maintaining rational credits,
scheduling crossings and storing machine states have additional costs.
In particular, arbitrarily tiny c_t cannot buy those controller operations
for free. Report that overhead separately or specify a price model that
covers it; the competitive statement must not silently become a complete
wall-clock or complete-economic theorem.

## A natural checked duty and its strongest controls

A proposed lemma j asserts that a named finite clause set K_j is
unsatisfiable. Its resumable prover searches for a checkable refutation;
some proposals can be satisfiable and never deliver one. A request asks
whether an action is warranted under a clause set F_t. A checked refutation
of any K_j subset F_t permits the certified action; otherwise a stipulated
safe fallback incurs c_t. The subset check warrants applicability. Clause
additions preserve an old refutation; deletions remove that applicability
unless its actual support remains. This is an explicit finite edit relation.

This example does not need scalar-only cost observations or unobserved
truth labels. Full certificates and their supports are retained. Fresh
incremental SAT with proof caching, ordinary lemma databases, unguided
round robin and the exact same covering scheduler are mandatory controls.
If the fallback itself solves F_t and produces a reusable certificate,
that stronger fallback must be represented as another paid reusable option;
our simpler nonreusable-fallback theorem is not the correct full comparison.

The intended delta would be an accountable scheduling/retention adapter,
not a new refutation calculus or a claim that conventional methods ignore
unresolved mathematics. Applicability preparation and proof checking must
be included in any practical experiment before an economic conclusion.
