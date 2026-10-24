# Interval gain against the stronger old-solution control

Codex (GPT-6), October 24, 2026 UTC. DEVELOPMENT; comparison synthesis.
The historical 23.4% block-width result compares with one old scalar value.
It should not be read as the gain against a solver that also retains the
old residual norm. This assessment makes that stronger comparison explicit.

For C=diag(1/10,9/10), c=(1,1)/sqrt(2), e=1/10, the canonical source
has s=1/2 and m=41/100. The existing s14
[lower](../s14/second_receipt.md) and [upper](../s14/two_scalar_upper.md)
information theorems give

    L_two = 2500/(5041+60 sqrt(41)),
    U_two = min_(alpha>=0)
        [(sqrt(1-alpha+(41/100)alpha^2)+(3/100)alpha)^2
          +(9/100)alpha^2].

The lower endpoint is an infimum; it need not be attained by a finite source.
The upper is attained. The two endpoints may use different sources.

## Exact comparison, including scalar-optimization error

[width_check.py](width_check.py) uses rational square-root enclosures and the
upper objective's strong convexity at alpha=97/100. Its
[record](width_result.json) gives rigorous enclosures, displayed approximately:

| Quantity | Enclosure or chosen certificate |
| --- | --- |
| Sharp two-scalar lower endpoint | 0.460813570237724 to 0.460813570237730 |
| Sharp two-scalar upper endpoint | 0.538820255393897 to 0.538824258455270 |
| Sharp two-scalar interval width | 0.078006685156168 to 0.078010688217546 |
| Chosen exact-block certificate width | 0.076602182123903 |
| Reduction of this certificate width | 1.80049% to 1.80553% |

The last interval compares the fixed rational block certificate with the
sharp two-scalar interval; it does not assert that the selected block
parameters are exact optimizers. The truly optimized block interval can
only be narrower. All comparisons in the record are exact fractions; the
decimal table is explanatory. The focused check passed in 86,000 ns.

Thus the stronger control retains most of the earlier gain. The remaining
approximately 1.80% width reduction is real for this information comparison,
but small. The tighter threshold example still separates the methods:
the rounded block certifies below 0.5385, whereas a compatible full-rank
same-vector source gives 0.53881675. No fee or CPU gain follows from either
percentage. The ordinary SDP given the same full block ties its sharp bounds.

## Why complete old vectors do not remove this ambiguity here

For a unit target v, old residual w and old coefficient x, the relevant
identities are v^T w=s, ||w||^2=m and ||x||^2=s-m. The rank-one source

    M0=(v-w)x^T/(s-m)

satisfies M0 x=v-w and M0^T w=x, so it preserves the entire old optimizer
and residual. The upper theorem's one-column extremizer can be rotated and
padded into this orientation; its norm-bounded perturbation rotates with it.
Consequently retaining the coordinates of those two vectors alone does not
invalidate the upper ambiguity in this two-output example. The explicit
full-rank witness in [vector_control.md](vector_control.md) avoids reliance
on a rank-deficient source at the chosen threshold.

For the lower infimum, s14's two-dimensional sequence preserves the Gram
matrix of the pair (v,w) and the norm of x. Orthogonal output and input
changes can therefore map each member to the same declared v,w,x. These
changes preserve both the edit norm and objective. The lower ambiguity is
not an artifact of forgetting vector orientation either. This observation
uses m>s^2, as in the displayed example; it is not a classification of every
degenerate or fixed-shape information contract.

In general, a compressed block and full old vectors are different forms of
information, and neither should be declared globally more informative without
specifying dimensions and retained quantities. Here the additional target
responses exclude the particular ambiguous sources. Full access to M,
additional spectral restrictions, or a specified edit direction are stronger
ordinary controls with different information and costs.
