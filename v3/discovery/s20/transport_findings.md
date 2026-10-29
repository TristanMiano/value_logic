# Certificate reuse: finite results and an exact worked radius

Codex (GPT-6), October 28, 2026. Same-model DEVELOPMENT; no readiness
credit is borrowed into the frozen V19-R/v1 contribution event.

The first [frozen run](transport_runs/a01/result.json) passed. Its
[records](transport_runs/a01/records.jsonl) retain changed models, exact
control certificates, all artificial families and their answers. There
were no executed failures or repairs. An indexing edit was corrected
during source review before the prospective freeze.

Twenty-one model controls include sixteen coefficient/receipt changes,
one revival of previously inconsistent receipts, and four receipt-budget
levels. The zero-budget level reused the old control certificate; twenty
new controls made312 numerical LP calls with exact rational acceptance.
The reuse calculation made zero new LP calls and enclosed every control
range and every nonempty control slice. This is an operation distinction,
not a measured speedup: certificate verification, rational dot products,
subset combination, storage and prior certificate production still cost
work. The finite check took1,083,779,900ns as one whole harness, including
controls; its unattended runtime earns no research-clock credit.

The first-hit recurrence agreed with exhaustive assignments on120
artificial families:88 finite radii,32 infinite, and8 zero radii among
the finite cases. Direct interval unions agreed at the tested budgets.
Four prescribed misuse cases were rejected. These tests do not establish
general soundness, security, or formal verification of this new code;
the [derivation](certificate_transport.md) supplies the mathematical argument.

## A meaningful, bounded decision consequence

For the inherited noisy-envelope example, enlarge both receipt intervals
from[-1,-99/100] to[-1-t,-99/100+t], retaining the physical models and
readout f(u,v)=u/2-3v/2. The previously rejected band is[-5/4,-6/5].
Retained certificates prove it remains rejected for every t<1/16.
The first outer hit is exactly1/16. At t=0,1/32,1/16, the transported
whole range equals the fresh exact control range. At t=1/8, the outer
range is[-3/2,43/200], whereas the exact range is[-281/200,-33/40].
Thus the method demonstrably loses precision after some old empty slices
can no longer be omitted. It does not assert a fictitious exact range.

For this particular band the sufficient radius is also sharp, by a new
hand construction. At t=1/16 choose

    block1 (u,v)=(113/400,371/400),
    block2 (u,v)=(371/400,345/400).

Their coordinate sums are121/100 and179/100, respectively, permitted
boundaries of the two old strips. Every coordinate lies in[0,1]. Each
minimum receipt is-371/400=-99/100+1/16. The two future values are-5/4
and-83/100, so their minimum is-5/4, entering the proposed band. The
uniform exclusion for all smaller budgets and this attaining source give
an exact first feasible budget here. This source was derived after the
run; it is not a prospectively predicted outcome or a general completeness
claim for certificate reuse.

## Failures that must stay visible

Changing an inconsistent constant receipt from[1,2] to[-1,1] revives every
old empty slice. The correct new range is[-4,2]; retaining their old empty
status would incorrectly return the empty set. Separately, changing the
objective from x to2*x on[0,1] makes the maximum2. Reusing the old upper
dual while discarding its residual would claim1; the sound residual bound
returns2. These are concrete counterexamples to tempting reuse shortcuts.

Disposition: retain as a useful conditional-reasoning adapter, with ordinary
safe-bounding antecedents explicitly credited. No standalone novelty claim,
promotion probability, or audit-fee saving is assigned. A next practical
question would compare certificate reuse and exact re-solving under an
actual repeated-query workload with complete cost accounting; that is not
required for the fixed V19 contribution.
