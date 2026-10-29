# P3-11-A1: interval bottleneck prior-work challenge

Codex (GPT-6), October 28, 2026. Same-model confirmation comparison.

The previously unavailable author PDF of Kasperski and Zielinski's
[Possibilistic Bottleneck Combinatorial Optimization Problems with Ill-known Weights](https://cs.pwr.edu.pl/zielinski/publications/papers/ijar.pdf)
was retrieved directly. Its title page is a September20,2010 IJAR preprint;
the journal article appeared in2011. An author-uploaded copy sits under a
2009 conference-page title, so that page's label should not date the file.
I read Sections2--3.1, Propositions1--3 and their AppendixA proofs, and the
Section4 scenario definitions. This is stronger than the earlier search lead.

The paper supplies robust/possible optimality and deviation calculations for
independent interval element weights and a fixed combinatorial family. Its
extreme-scenario arguments already exploit bottleneck structure. V19 does
not invent interval bottleneck inference or robustness. The read results do
not condition a shared affine source on several earlier optimum reports and
return the entire new scalar image with the stated receipt-parameter bound.
That distinction survives this comparison; it is not a proof of priority.

## Mathematical distinction reconstructed for this review

The following argument is ours, not a quotation or claimed new general fact.
On a single interval box Gamma, each configuration's bottleneck is continuous.
The optimum over a finite nonempty configuration family is also continuous,
as is the difference between a fixed configuration's value and the optimum.
Because Gamma is connected and compact, each such scalar image is a compact
interval. Computing its two endpoints can therefore recover its entire image.

V19's local slices are connected, but its source after shared scalar receipts
can be disconnected. The same continuity argument cannot replace the whole
output by its hull. Moreover, its local interval labels (i,T) are not one
joint scenario of unrelated uncertain weights: labels for the same block
come from overlapping/nested restrictions of one source variable. Only the
one label selected per block in a partition is used at once. Treating all
labels as independent simultaneous weight observations changes the model.

There is still strong overlap. V19's outside calculation is a deterministic
bottleneck optimization over feasible subset partitions. Standard bottleneck
and semiring machinery solves that calculation. The remaining assessment is
whether the explicit conditioned-source reduction, full-image clipping,
resource accounting and witness/certificate contract together constitute a
useful moderate synthesis. The prior result narrows that claim; it does not
support a new bottleneck primitive, a new robustness concept or a strict
advantage over an ordinary implementation of the same reduction.

## Exact set-estimation access limitation

The author-hosted Espindola-Winck--Hardouin--Lhommeau2024 manuscript timed out
in browser retrieval and a20second direct retrieval. The HAL copy returned
an access-denial page; no challenge or access control was bypassed. The
[publisher's introduction](https://www.sciencedirect.com/science/article/pii/S0005109824003935)
explicitly describes exact conditional reach sets and a concise max-plus
polyhedral representation. That conceptual achievement is credited. Its
technical proofs have not been reconstructed in this attempt, so it cannot
be reported as a fully excluded theorem-level competitor. The existing
max-affine fitting and ordinary semiring comparisons remain the strongest
fully worked overlap checks here.
