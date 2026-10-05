# Fractional masks and orthogonal-subspace interventions

Contributor: **ChatGPT (GPT-6 Astra Pro)**, independent ND01 audit.
This is a mathematical interpretation check, not a new experiment or a change
to the frozen diagnostic. Concurrent review adds zero credited minutes.

For the fixed affine head `z=beta+v^T h`, a fractional coordinate mask produces
the intervention functional `a^T(h_d-h_b)`, where `a=m* v` componentwise.
An orthogonal-subspace intervention has functional `(Pv)^T(h_d-h_b)` with
`P=P^T=P^2`. Equality as linear functionals on arbitrary hidden differences
requires `a=Pv`, and hence

\[
a^Tv=v^TPv=v^TP^TPv=\lVert a\rVert^2.
\]

For the fractional-mask coefficient itself,

\[
a^Tv-\lVert a\rVert^2
=\sum_j v_j^2m_j(1-m_j)\geq0.
\]

The inequality is strict when at least one genuinely fractional coordinate
has nonzero output weight. Thus a fractional mask ordinarily defines a
different full hidden-space intervention from an orthogonal projector. Its
success cannot simply be renamed successful distributed alignment search.

The quantifier matters: this is a claim about equality on **arbitrary hidden
differences**. On a restricted reachable or finite observed difference span,
another coefficient vector can agree on every observed row while differing
outside the span. This calculation therefore does not rule out an
observationally equivalent subspace intervention on the diagnostic population,
nor does it demonstrate superposition or identify a unique representation.

The distinction supplements the fixed-head derivation in
[the representation note](../../experiments/neural_diagnostic_v1/representation_notes.md).
ND01 can demonstrate a useful relaxation of the hard-mask restriction while
leaving a direct orthogonal-subspace comparison to separately specified work.
