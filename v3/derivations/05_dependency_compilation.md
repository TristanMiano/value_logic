# P3-05 — Checked finite dependency compilation

Contributor: **ChatGPT (GPT-6 Astra Pro)**, October 8, 2026 UTC.
Status: S3 finite construction complete. The finite program grammar below is a new
front-end to the [portfolio receiver](05_portfolio_transport.md); it is not an
unrestricted code-equivalence or causal-model discovery procedure.

## 1. The missing bridge

A verified inequality for an expression named `new-minus-old` does not prove
that the expression describes the intended change. The consumer supplies two
versioned programs, one shared Boolean input signature, output labels and known
rational loss coefficients. The receiving procedure independently compiles
those inputs. The proof then has to match that constructed difference, source,
rank, unit and full request record. This is a finite analogue of current-request
matching, not an authentication of the external provenance of the programs.

A program is a finite ordered, acyclic collection of Boolean definitions.
Leaves are input coordinates and constants; operators are Boolean negation,
conjunction, disjunction and exclusive-or; a call applies an explicitly supplied
finite Boolean truth table to arguments. References may name only earlier
definitions. All definitions, including unused ones, are validated. Table
identities are distinct even when their tables agree: changing the `live` table
does not change a separately identified `copy` or `original_predictor` table.
Inputs denote the same quantities in the two programs. A different dependence
assumption requires an explicit different signature or a supplied transport map.

There are no loops, unknown code bodies, hidden evaluator answers or consistency
oracles in this grammar. Its full finite truth tables are received input data,
whose construction and adequacy are not provided for free. Input/expansion caps
are operational restrictions, not a claim that arbitrary mathematical values
are bounded or that all logical counterfactuals have this representation.

## 2. Compilation and conditional correctness

**CT05-12 — finite compilation.** Compile each definition in topological order,
substituting previously compiled references. For a table call, form the
conjunction of the appropriate argument or negated-argument literals for each
input row whose output is one, and take their disjunction. A table with no one
row compiles to zero; a zero-argument one table compiles to one. Construct
exclusive-or as $`(a\land\neg b)\lor(\neg a\land b)`$.

For every admitted input vector, the compiled expression equals the program's
ordinary Boolean evaluation. Proof is by structural induction on each finite
expression and then induction on definition order. Exactly one full input-row
conjunction is true for a table call; hence the disjunction has its specified
output. The proof uses the complete supplied table, not observations of a few
calls. Sharing a definition in syntax does not change its Boolean denotation;
actual evaluation/compilation costs remain separately recorded.

With known rational coefficients $`w_o`$ and common units, set

```math
 d(x)=\sum_o w_o\bigl(P_{\mathrm{new},o}(x)-P_{\mathrm{old},o}(x)\bigr).
```

Each output is a Boolean source expression and each coefficient is known.
This remains inside the admitted rational piecewise-affine loss grammar;
there is no product of two jointly uncertain real quantities. A common
additive cost cancels; action-specific changes must instead be included in the
request. This front-end currently requires the same supplied coefficient table
on both sides, not arbitrary new objectives.

**CT05-13 — composed receiving guarantee.** Independently compile the requested
old/new program pair and source constraints; verify the portfolio proof against
that exact frame and an adequate requested bound $`B`$. The accepted result
implies $`d(x)\le B`$ on every currently minimal admissible repair, subject to
the portfolio theorem's nonempty-source and coverage premises. This follows by
CT05-12 plus CT05-6–8. It is a formal conditional guarantee about the supplied
programs and model. It does not show that the model represents physical
predictors or another agent's actual reasoning.

The calling action/program pair is fixed independently of the hidden input.
Choosing a different proof on different covered cases is permitted; changing
the action pair per case is not. Receiver recompilation is charged, even when a
cached proof supplies the inequality. Merely attaching a program ID to an
unrelated numerical term is rejected by request binding.

## 3. Dependency preservation and its boundary

**CT05-14 — sufficient component preservation.** For a requested output,
collect all referenced definitions and tables transitively, as well as its
root expression and input signature. If those exact components are unchanged,
the output's compiled denotation is unchanged on every input. Induct on its
finite dependency subgraph. Edits outside that support can therefore preserve
this semantic output, provided the entire new input remains admitted.

This is ordinary dependency reasoning specialized to the compiler, not a new
general slicing theorem. The converse is false: changing a used table or
rewriting an expression can preserve its extensional output. A syntactic
support check is conservative. Names or digest equality alone do not prove
semantic identity; rehydrating a saved cache requires its declared checks.

Two programs can agree on every unedited output while having different edit
behavior. If one output reads `live(h)` and another implementation reads a
separately named `copy(h)` with identical initial truth table, replacing only
`live` separates them. Therefore observational agreement—even exhaustive in
this finite input space—does not identify replacement routing. This is the
existing causal/logical dependence obstruction in an executable front-end.
It is not evidence that values cannot encode a graph when the graph is supplied.

Renaming all component identities and consistently transporting references
preserves extensional outputs, but not necessarily compilation work or textual
support sets. An interface correspondence has to carry the edit targets too.
A blanket equality of all counterfactuals cannot be inferred from observational
function equality. The primary causal-abstraction comparisons are recorded in
[the S3 source cards](../literature/05_portfolio_sources.md).

## 4. Fixed development target

Let the shared input be $`h\in\{0,1\}`$. Three separately identified initial
truth tables `live`, `copy` and `original_predictor` all return $`h`$.
The old outputs A/B call `live`; C calls `copy`; P calls `original_predictor`.
Use cost $`6+A-2B-C-2P`$, and keep the output roles fixed.

Replace `live` by $`1-h`$ while leaving the copy and original predictor intact.
The new-minus-old difference is $`-1+2h`$. Under hard condition $`h=0`$ it is
$`-1`$; after withdrawing that condition its sharp uniform upper bound is one.
At $`h=0`$, changing only A gives difference one, changing the shared live
function gives minus one, additionally changing the copy gives minus two,
and explicitly changing the predictor as well gives minus four. The changes
are distinct requests, not four estimates of one unspecified intervention.

The receiver must reject an old minus-one bound on the withdrawn source, accept
a correctly penalized bound of one, and reject replacing the requested new
program by a more favorable program while leaving the proof untouched. These
are prespecified DEVELOPMENT tests of the formal interface, not empirical
judgments about how a real predictor would respond.
