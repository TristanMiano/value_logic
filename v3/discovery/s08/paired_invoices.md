# Checked paired invoice contrasts under a shared row

**Prospective DEVELOPMENT derivation — Codex (GPT-6), October 14, 2026 UTC.**

The source-free bandit pays for exploratory requests whose complete
acquisition bills contain common variation. The original geometry idea
suggests a smaller learning target: compare two policies on the **same**
latent row and cancel shared fee contributions. No Markov source model is
needed to define the contrast. Optional second-policy execution reuses
already paid observations, buying only nodes its trace still needs.

Separate completion intervals yield a valid but potentially loose contrast
interval $`[L_i-U_j,U_i-L_j]`$. They choose their extrema in different
worlds. A sharper certificate must use one shared compatible world:

```math
L_{ij}(z)=\min_{x\sim z}(C_i(x)-C_j(x)),\qquad
U_{ij}(z)=\max_{x\sim z}(C_i(x)-C_j(x)).
```

A finite decision diagram is a conservative first representation. Its
producer may enumerate binary middle/extreme indicator worlds; the checker
must independently execute both supplied policies on every terminal path,
verify all branch scopes and verify the local min/max equations. A reduced
ordered diagram can merge equal subfunctions and remove tests with identical
children, but its setup and retained size are paid. No polynomial size bound
is assumed. Exact contrast certificates are conditional computations,
not newly acquired physical data.

Before implementing a general service, perform one small finite screen:
n=3 through 10, two predetermined positive-fee vectors per size, the five
existing policy proposals, every unordered distinct-root pair. Enumerate
the complete indicator truth table to build a canonical ordered algebraic
decision diagram (ADD) for each invoice and their paired difference. Use
the natural node order first, without selecting a favorable order after
seeing results. Count all policy/world executions and diagram nodes.
Check reduction identity against the unreduced truth table, and exact
paired ranges against separate ranges. On the n<=6 cases also enumerate
every partial receipt pattern. Larger partial screens use a fixed seed
and at most 128 patterns per pair. Save all outcomes and negative controls.
If the contrast does not contract enough to repay construction or the
diagram grows badly, retain that screen and stop this representation.

The ADD is an ordinary symbolic representation. Its value here would be
the paid connection from original-source receipts to a small contrast,
not novelty of diagrams or common random numbers. A subsequent randomized
completion estimator is the already identified control-variate method.
Do not infer a statistical claim from the finite diagram screen.

## Compositional extension after pi01

The finite screen contains distinct root maps with identical invoice
functions. Some differences occur only in unreachable interval states;
others can be genuine equal-fee alternatives. Exact root-map deduplication
therefore leaves redundant learning arms. An all-world invoice identity
would justify retaining one representative for the fixed-bank mean-fee
objective, even when the policies have different action traces. It does not
justify substituting traces when another downstream duty depends on them.

Truth-table enumeration is avoidable for this restricted policy language.
For every interval and mode compile the invoice function from smaller
interval functions. For queried node i, let E and M be the sums of the
extreme and middle child functions prescribed by invoice_completion.py.
Then the exact original-source recurrence is

```math
C_{a,b,m}(x)=c_i+(1-x_i)E(x)+x_i M(x).
```

An ordinary singleton contributes zero. The queried variable does not occur
in either child. ADD addition, scalar addition and an ordered ITE operation
compile these recurrences bottom-up. A separately implemented checker can
validate each recurrence by Shannon cofactoring its proposed result and
operands; it need not enumerate all worlds. Induction on interval length
then binds the final ADD to the supplied acquisition policy. Canonical
roots shared by two admitted final diagrams prove invoice equivalence.
Subtracting two diagrams gives a paired contrast; min/max abstraction over
unobserved variables gives exact conditional extrema.

No worst-case polynomial ADD size follows. The number of interval
recurrences is quadratic, while each apply/check can depend on products
of diagram sizes. Quote actual node creation, cofactor checking and retained
bytes; a compact final root alone hides intermediate compilation work.

Prospective next cap: recompile the 16 pi01 fee vectors, compare all complete
small truth tables, then six vectors at n=16,32,64 (two each; fixed seed
8141501). Abort a unit above 250,000 created nodes or 2,000,000 apply states,
preserving the charged partial work. No physical audits or confirmation
claims. Use a natural increasing variable order fixed before execution.
