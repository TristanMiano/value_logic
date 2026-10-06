# F16 core reconstruction — initial save before proof comparison

Contributor: **ChatGPT (GPT-6 Astra Pro)**, delegated distinct reconstruction.
Base commit: `6ef27f20e3ac0920953a27dd84d6c91a021ba58f`.
Date: 2026-10-05 UTC. Initial reconstruction completed after the bounded probe
at **22:04:29 UTC**; this file is saved before opening the derivation proofs.

This is a definitions-first reconstruction within the same project/assistant
environment, **not a fully blinded external review**. Delegated concurrent work
contributes **zero principal minutes**. This work does not attempt Gates C/D or
F17 and does not modify the core, historical evidence, clock, or time ledger.

## 1. Information boundary before this save

Files opened before the save:

- `v2/checks/f05_semantics.py`: requested the whole file in the first batch;
  aggregate output was truncated. Subsequently inspected lines 1–510 directly,
  including all semantic definitions and the beginning of its example tests.
- `v2/checks/f06_inference_rules.py`: requested the whole file in that batch;
  aggregate output was truncated. Subsequently inspected lines 1–360 directly,
  including the complete normalizer, native checker, builder, and RHS replay.
  The first batch also exposed the file's example/test section.
- `v2/notation.md`: read in full. It contains summaries and references to later
  claims, including target-unit completeness and current-request binding.
- `v2/project_spec.md`: requested in full, with truncated aggregate output;
  explicitly inspected the relevant current semantic/inference/acceptance
  sections at lines 360–850, and its headings/reference matches. Its opening
  requirements and historical summaries were also visible in the first batch.

Repository HEAD was checked. No applicable `AGENTS.md` was found by a repository
file search or by checking the ancestor locations. No file under `derivations/`,
no gate review, and no new F16 root review has been opened before this save.
The two Python modules import only the listed F05 definitions and the standard
library; no further implementation import was needed.

The code below was imported with `PYTHONDONTWRITEBYTECODE=1`. Only five bounded
probes were run; no test suite or neural run was started. The mathematical
reconstruction below is not an inference from those probes passing.

## 2. Independent semantic statement

Fix a finite signature with declared source-coordinate units and named positive
rational conversion factors. Interpret a source coordinate as one shared real
number throughout the term and the source rows. Interpret a lexical local using
the environment in effect at its binder. Literals, addition, rational scaling,
minimum, maximum, residual `max(b-a,0)`, and conversion have their ordinary
finite-real meanings. Every well-typed finite term is total, continuous, and
piecewise affine; an individual value is finite even when the domain and value
range are unbounded.

For one case h, let D_h be all assignments satisfying that case's affine rows.
The context's supplied rational witness establishes D_h is nonempty. A global
domain is the union over the nonempty, distinct live case list. The comparison
means `eval(new)-eval(old) <= budget` on the requested local domain or on every
case of the union. This meaning is specified before and independently of proof
acceptance.

The point evaluator's accepted input coordinates are rational; the proposed
universal theorem concerns the evident finite-real extension of the same
operations. Exact rational point evaluation alone cannot prove that theorem.
For these rational affine rows, a nonempty real polyhedron has a rational point,
but the code does not need to infer that fact: a concrete feasible rational
witness is required for every live case.

## 3. Normalization must be proved before using rewrite

The normal form is a finite rational linear combination of atoms plus a
constant. Atoms are either identified source coordinates or min/max nodes
whose children are already normalized forms. Assign a denotation to forms by
linear evaluation and to nonlinear atoms by the indicated min/max operation.
Induction over `go(node, env)` shows that its result denotes the original term.
Collection, deletion of zero coefficients, and constant folding preserve this
denotation. Residual is expanded to its defining maximum.

The lexical environment stores the *normalized RHS value*, not the name of a
local placeholder. The RHS is processed in the old environment; the body is
processed after shadowing. Therefore two occurrences of a nonlinear local body
with different RHS values do not collapse into one atom. Source names and
local names use different namespaces. A free local in its own RHS is rejected,
so ordinary `let` introduces no recursive fixed point.

Typing is checked recursively before zero multiplication can erase a child.
Forms do not retain intermediate unit names, but equality of numeric forms is
still sufficient for numeric equality: declared conversions are exactly their
numeric factors, and `same_difference` also requires all four compared outer
terms to have the same unit. This is a sufficient equality procedure, not an
oracle for every semantic identity. For example, min's symmetry is not itself
an affine collection identity.

This establishes the obligation needed by constant, rewrite, shared-middle,
and shared-query checks without invoking rule soundness or completeness.

## 4. Native rule induction, including signed budgets

At a fixed admitted assignment, write `a-b <= beta` for each parent. The
checker requires parents to be strictly earlier, so induction is well founded.
All non-case rules preserve the same local/global case designation.

| Rule family | Reconstructed preservation argument |
|---|---|
| constant | A constant collected difference has exactly that value at every assignment. |
| row | If `lhs-rhs = a.x+c`, the admitted row says `a.x <= -c`; `normalized_row` removes c and returns budget `-c`. |
| rewrite | Equal collected differences have equal denotations. |
| trans | Equal middle denotations cancel; add the two signed inequalities. |
| add | Add the two inequalities at the same assignment. Duplicate use duplicates both expression and budget. |
| scale | A nonnegative rational k preserves the inequality and multiplies the budget by k. |
| negate | `(-old)-(-new)=new-old`; swap the pair and retain the budget. |
| convert | Multiply the difference and its budget by the declared positive factor. |
| slack | Adding a fixed nonnegative amount weakens the bound. |
| meet_proofs | Both bounds apply to the same difference, so their minimum applies. |
| max_common | `max(a,c)-b = max(a-b,c-b)` for a shared old term. |
| min_common | `a-min(b,d) = max(a-b,a-d)` for a shared new term. |
| congruence | Put e=max(beta,gamma). Coordinatewise bounds by the same e, monotonicity, and `min/max(x+e,y+e)=min/max(x,y)+e` give the result even when e is negative. |
| res_congruence | The unclipped new residual input changes by at most beta+gamma, with the first operand reversed. Clipping at zero gives bound max(beta+gamma,0). |
| lattice | The four projection/injection inequalities have budget zero by ordinary real min/max order. |
| all_cases | Every live case occurs exactly once, the literal expression pair is unchanged, and the maximum of the local budgets applies to the union. |

The residual clamp is necessary. Replacing -1 by -2 improves an unclipped value
by -1, while `max(-2,0)-max(-1,0)=0`. A residual rule that propagated the negative
budget without the zero maximum would be false. The actual code has the clamp.

The induction is source-relative. Neither row acceptance nor the feasibility
witness establishes empirical truth, proxy adequacy, or policy availability.
Those are additional interpretation premises, not results of this kernel.

## 5. Shared information, case union, and composition attacks

### 5.1 Shared-source cancellation

Suppose the two component rows are

`(N1-O1)-theta <= -3/4` and `(N2-O2)+theta <= 1/4`.

Adding them at the *same* theta proves the combined difference is at most
`-1/2`. That inference retains joint information and does not optimize each
component separately. Replacing theta by independent `t1,t2` leaves `t1-t2`
in the difference. The explicit feasible assignment

`N1=N2=1/4, O1=O2=0, t1=1, t2=0`

satisfies the two renamed rows at equality, yet the combined difference is
`+1/2`. The code rejects rewriting the renamed-row sum to the source-cancelled
query. This is the expected defense against lost alignment.

Actual sequential execution still needs an interpreter explaining why total
cost is the displayed sum, which downstream state is shared, and which choices
are legal. Additive term soundness is not automatically a theorem about every
physical composition of programs.

### 5.2 Case selection and vacuity

An empty list of live cases is rejected, and each live case has a feasible
witness. No contradiction can be installed as a live row set and then used
as evidence for a requested improvement. A branch-specific proof does not
automatically become global: all cases are required, not a favorable subset.

The `all_cases` constructor requires the identical literal new/old pair. It
cannot combine “choose A in case h1” with “choose B in case h2” into a claim
about a single unobserved-case policy. An external policy interpreter must
still keep hidden assignments/cases unavailable to policy choice; the term
checker does not itself authenticate that interpreter.

### 5.3 Circularity attempts

The proof graph cannot cite itself or a forward step. Lexical bindings are
nonrecursive. A numerical source may name a report or a later output, but its
presence is an assumption with an explicit source interpretation, not a proof
of the correctness of a program producing that quantity. None of the sixteen
rules turns a predicted proof budget into source validity. A stronger cyclic
interpretation would require separately supplied semantics.

## 6. Unit reachability and a noncircular conversion lemma

For output unit u, define A(u) as units with a directed conversion path to u,
including u. Every source coordinate occurring in a well-typed u-term has its
unit in A(u). Every ancestor of a u-root has a unit in A(u): non-conversion
rules preserve unit, and a conversion ancestor has a path onward to u. Hence
only rows whose unit is in A(u) can supply assumptions to that root.

Let the u-reduct retain exactly those rows. The same pointwise rule induction
therefore proves an accepted u-root on the reduct domain, even where an
unreachable row of the full source fails. This is stronger than the ordinary
full-source soundness statement and supplies a direct incompleteness test.

Minimal witness: units U,V, one source `x:U`, one conversion `up:U->V` with
factor 1, and the sole row `up(x) <= 0_V`. The context has witness x=0. The full
source implies `x <= 0_U`; the U-reduct has no rows and admits x=1. A native
U-proof of that comparison would contradict reduct soundness. This is a
full-source completeness obstruction, not a soundness failure.

One must not assume that the normalizer directly distributes a conversion
through min/max. Its atom representation generally does not. Here is a
noncircular derivation sufficient to remove that concern. For positive k,
min projections followed by scaling and `min_common` prove

`k min(a,b) <= min(ka,kb)`.

Apply projections to min(ka,kb), scale by 1/k, use `min_common`, and scale back
to prove the reverse inequality. These are same-unit native derivations.
If conversion c has factor k, convert the latter derivation and scale by 1/k.
The resulting forms rewrite to

`min(c(a),c(b)) <= c(min(a,b))`.

The other direction comes directly from converted projections and
`min_common`. Maximum is analogous. A factor-2 V->U implementation of this
construction checked both zero-budget directions using fourteen native nodes.
It does not use order reflection, inverse conversion, or a completeness oracle.
Paths compose this argument; inverse *numeric scaling in the target unit* is
different from introducing a reverse unit edge.

## 7. Independently reconstructed characterization route

The following gives a concrete route whose hypotheses must be compared with
the later proofs. It does not take their theorem statements as an axiom.

1. Grammar induction gives each u-term a finite global rational affine-piece
   list in the accessible coordinates. For a difference f, refine by all
   pairwise equality hyperplanes of these pieces. On each full-dimensional
   arrangement cell R, f selects one affine piece. Choose the pieces whose
   values at an interior point are at least f there; call that set I_R.
   Then `m_R=min_{j in I_R} l_j` equals f on R and is at most f everywhere.
   The latter claim follows along a line segment from the interior point:
   an affine-piece order can cross only once; a switch taking f below all
   initially upper pieces would require the opposite crossing direction.
   Thus `f=max_R m_R`; continuity extends equality to arrangement boundaries.
   This is a global finite max-min construction from the term's pieces, not
   a consequence of the intended native completeness theorem. Degenerate
   duplicate pieces and the zero-dimensional constant case can be removed
   or handled directly.
2. For one nonempty reduct polyhedron `Ax<=eta` and one clause
   `min_j(a_j.x+c_j)`, maximize y subject to those rows and
   `y-a_j.x<=c_j`. Its bounded finite optimum has a rational dual witness
   `lambda>=0, mu>=0, sum(mu)=1, lambda A=sum_j mu_j a_j`, with bound
   `lambda.eta+sum_j mu_j c_j`. This is the ordinary finite rational linear
   optimization step; an implementation must actually supply/check the
   witness rather than infer it from a sampled optimizer result.
3. The witness has a native realization: min projections, weighted addition,
   and `sum(mu)=1` give `min_j l_j <= sum_j mu_j l_j`. The nonnegative
   weighted source rows bound the affine combination. Transitivity gives
   the clause bound; max joins combine clauses. Forward conversion paths
   and their positive numeric normalization put the relevant rows and
   expressions in u. Exhaustive case maximum finishes the union.
4. No source reduction is justified merely because individual marginal
   ranges match. Full-source and reduct conclusions coincide only when
   the relevant projected joint domains support the same queries. Equality
   of their projected unions is an evident sufficient condition; finite
   CPWA characteristic violation probes offer a route to necessity.

For an existing globally defined native term over a nonempty finite union of
closed rational polyhedra, a finite maximum is attained and rational: refine
into finitely many closed affine cells and use the bounded affine optimum on
each nonempty cell. Consequently strict validity everywhere implies a strict
native rational budget if the preceding completeness construction succeeds.
This attainment argument must not be transferred to arbitrary open source
sets, arbitrary continuous functions, or an unattained infinite-family limit.

The unit reconstruction and the max-min/dual route provide independent proof
content; comparison still needs to inspect the exact later claim scopes,
especially local extension claims and use of the max-min theorem itself.

## 8. Current-request receipt is an additional obligation

`f06_inference_rules.check(ctx, proof)` receives no separately supplied request.
It certifies the root which the proof itself contains. At a context with a
free `x:U` and witness x=1, the global constant proof `0 <=[0] 0` is accepted.
The different requested claim `x <=[0] 0` is false at that admitted point.
This is a minimal demonstration that a valid trace is insufficient as a
receiver for an arbitrary external request, not a counterexample to the
kernel's advertised root-soundness contract.

A current receiver must independently bind the current context, requested
case/domain, literal new/old terms and unit, then verify that the checked root
budget is no larger than the requested inclusive budget. Exact case equality
is a conservative acceptable receiver convention; a more permissive convention
would need a proved domain inclusion. A copied context fingerprint only binds
the supplied syntax/metadata; it does not establish empirical source meaning
or authenticate an external program. Revision of a report that controls the
program requires binding the new expression/program interpretation as well.

The specification says a receiver exists, but its implementation/proof is
intentionally not opened yet. Whether it closes this obligation is reserved
for the post-save comparison.

## 9. Bounded probe results and initial status

| Probe | Exact result |
|---|---|
| Wrong external request beside a valid constant root | Root budget 0 accepted; requested x-vs-0 gap is 1 at a feasible point. |
| Factor-2 forward conversion of min | Both directions accepted at budget 0; fourteen nodes. |
| Independently renamed component uncertainties | Cancelled rewrite rejected; feasible combined gap is +1/2. |
| One-way U->V source row | x=0 is full-feasible; x=1 is not full-feasible but is admitted by the empty U-reduct. |
| Saturation after signed improvement | Unclipped change -1; clipped change 0. |

**Initial disposition:** no native-rule soundness counterexample found. The
request-binding and target-reduct qualifications are necessary and have exact
witnesses. They are not yet recorded as defects because the specification
already advertises separate receiving and reduct scope. The next stage is to
compare this saved reconstruction against the existing soundness and
characterization derivations and follow the dependencies needed to determine
whether their actual statements satisfy these obligations.
