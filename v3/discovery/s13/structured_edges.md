# Invoice charging on a structured unresolved source

Codex (GPT-6), DEVELOPMENT, October20,2026. A channel-specific adaptation of
ordinary adversary/certificate lower-bound ideas, not a new general lower-bound
method. Uses the local mass-tree lemma in invoice_rate.md.

Let S be any finite set of Boolean worlds with uniform law and target f.
Choose undirected pairs{x,y} with f(x)!=f(y) and nonnegative weights w_xy.
Require, for every world x and queried coordinate i,

```math
\sum_{y:y_i\ne x_i} w_{xy}\le1.
```

At the first private query where the two worlds diverge, each separated pair
is charged to that query node. The weighted incident load at each endpoint
is at most one. Therefore the total charged edge weight at the node is at
most the smaller number of worlds in its two branches, exactly the bound
used for cube edges. If both branches stop immediately, their invoices agree
and this node separates no pair. The same abstract-tree recurrence gives

```math
\mathbb E[\mathrm{fee}]\ge
 \frac{2\beta(H,f_0)}{|S|}\sum_{\{x,y\}}w_{xy}
```

for zero-error termination, where f_0>=0 is the fixed episode fee (distinct
from target f). Repeated queries, arbitrary adaptive public choices and
independent coins are handled as in the original argument. This is not a
beta multiple of the *optimal ordinary query complexity*: the displayed
adversary relaxation may be far weaker than that optimum.

For a nonuniform source p, layer-cake integration gives
2beta*sum w_xy*min(p_x,p_y). Constructing or optimizing the weights can be
exponential in the description of S; the inequality is not a free controller.

## Affine-source specialization

For a checked affine source x0+V and a nonconstant parity target t.x, choose
nonnegative weights w_g on directions g in V with t.g=1. Put that weight on
each pair{x,x+g}. The coordinate-load condition becomes

```math
\sum_{g:g_i=1}w_g\le1\quad\text{for every }i.
```

Each direction contributes |S|/2 undirected pairs, giving lower bound
beta*sum_g w_g. This is a fractional packing of target-changing directions.
Its dual assigns coordinate weights whose sum on every such direction is
at least one, a standard fractional certificate form. Integral coordinate
selection may be harder and may have a gap; no exact source-general optimum
is asserted. Full-cube parity recovers the earlier n*beta bound by selecting
the n unit directions.

For a repetition source with only two worlds, this general cap-dependent
bound need not be sharp. A one-bit invoice encoder costs3/2 query units at
equal source weights even if H is large; the relaxed mass tree can use branch
patterns unavailable to the tiny source. This identifies a useful limit of
the extension rather than a reason to claim universal optimality.
