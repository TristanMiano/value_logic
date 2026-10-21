# A finite reset-price correction and an information threshold

Codex (GPT-6), DEVELOPMENT, October20,2026. Combines s11's established
invoice-composition degree bound with the new edge price. No new polynomial-
method theorem or new block decoder is claimed.

For n fair bits, cap2<=H<=n and full parity, put q=ceil(n/(H-1)),
beta0=1+1/(2^H-2), and beta_f=beta(H,f). An invoice event from one episode has
Boolean polynomial degree at most H-1: its last purchased answer cannot alter
its bill. Along a fixed public transcript of e episodes, multiply its fixed
episode-event polynomials. The transcript degree is at most e(H-1), including
adaptive choices made from earlier public bills. This is the exact composition
fact already proved in s11/invoice_composition.md.

A nonempty full-cube transcript on which parity is constant has a nonzero
full-parity Fourier coefficient, and hence degree n. Therefore *every*
terminal path of an exact protocol requires at least q nonempty episodes.
This is stronger than merely finding one expensive path. Conditioning on
independent coins handles randomized exact protocols as before.

The query-only edge bound still applies to a strategy selected in response
to positive reset prices. Adding the separately justified reset requirement
gives the finite lower bound

```math
\mathrm{OPT}\ge
\max\{\beta_f n,\ \beta_0 n+qf\}.
```

The inherited q-block parity encoder costs exactly n+q/2+qf in expectation.
Thus a completely explicit upper/lower gap is at most

```math
\frac q2-\frac{n}{2^H-2},
```

independently of the reset tariff. The richer adaptive menu may improve the
upper bound. For H=n, q2 and the displayed gap is below one query-fee unit,
even for very expensive resets. This usefully strengthens an asymptotic rate
whose finite remainder can otherwise conceal a large extra reset.

An example inside the already available adaptive menu shows why its old
fixed-block control must remain strong. At n3,H3, first run a two-bit prefix.
If it resolves one bit, decode the remaining two-bit parity in one final
episode; if it resolves two, signal the last bit in one final episode. The
expected query fee is7/4+(1/2)(5/2)+(1/2)(3/2)=15/4, always with two episodes.
Thus it costs15/4+2f, better than three-bit fixed blocks'4+2f. This is an
analysis of the inherited adaptive control, not another new algorithm gain.

## The same correction for partial statistical information

In partial_information.md's parity-tilted family, a transcript with fewer
than q episodes has parity bias zero by the same degree argument. Consequently
J=E[m_T^2]<=P(e_T>=q), and E[e_T]>=qJ. Combining this with the query-only
information bound yields

```math
C\ge \max\{\beta_f n,\ \beta_0 n+qf\}\,J.
```

Together with the exact block experiment, this bounds the optimum C/J within
the same tariff-independent additive gap above. Zero-information experiments
are excluded when taking the ratio. Private coins can be revealed for the
lower-bound argument and then removed by conditional Jensen as in the earlier
note. The contract still excludes preparation/controller/coin prices and
additional observations. This is a derived finite bound, not an application
measurement or independent confirmation.
