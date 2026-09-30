# F08 reconstruction and acceptance argument

Research contributor: **Codex (GPT-6)**, September 30, 2026 UTC.
Review type: fresh reconstruction by the same assistant. No independent human,
external model or proof-assistant review is claimed. Task closure and actual
time are recorded in [S1](../work_logs/F08_2026-09-30_S1.md); this proof record
does not by itself certify that the protected minimum has elapsed.

## 1. The accepted mathematical question

The conjecture that the unchanged native calculus is complete for every
admitted full source context is false. The factor-one U->V example in
[04 section 1](04_characterization.md) has a feasible V row bounding x:U,
but no path returning that evidence to U. A rational model of the U-reduct
refutes the requested U bound. This is a structural nonderivability argument,
not the failure of a proof-search program to find a certificate.

The replacement theorem is exact: for finite rational typed CPWA syntax,
positive rational conversions, and a nonempty finite union of feasible closed
rational polyhedra, the native global consequences in unit u are precisely the
semantic consequences of the u-reduct. The reduct retains exactly those rows
whose units can reach u. It is computed from syntax and the conversion graph,
before knowing which queries hold. Thus the characterization does not define
the represented source information by equality of all answers.

An optimal finite native budget is rational and has both a finite proof and a
rational attaining reduct model. Otherwise the native optimum is infinite;
infinity is a metatheoretic status, not a permitted literal proof budget. Full
source completeness has the separately stated fixed-signature, graph-uniform
and individual-context criteria U7, U8 and U10. None can be replaced by the
claim that every full-source semantic inequality is already native.

## 2. Reconstructing the necessity direction

Start with a well-formed finite proof, not a numerical optimizer's output.
Check all its stored instructions, then inspect the ancestors of its root.
Every premise edge either preserves the inequality unit or follows a named
positive conversion edge. Consequently every used row's unit reaches u.
Every used row remains true in its own reduct case.

Induct over this sub-DAG with an explicitly indexed domain: a local statement
holds in its named reduct case, and a global statement holds on their union.
The all_cases rule takes one proof for every live case with the same literal
pair, so it assembles the union without assuming simultaneous membership in
all cases. The other native rules preserve their already established domains.
This gives the root inequality throughout the reduct.

Two details matter. First, an unused foreign let binding is a counterexample
to a purely syntactic leaf-dependency claim. The typed-environment induction
in 04a B proves the denotational dependence actually needed. Its binding RHS
uses the old environment; shadowing is accounted for. Second, dropping rows
changes proof indices and context fingerprints. This mathematical induction
does not accept the old serialized proof in a changed context without
reconstruction and checking.

## 3. Reconstructing sufficiency without an oracle

There are two explicit construction routes. They share elementary rational
linear elimination and certified unit retyping, but differ in how they handle
nonlinear expressions. Neither asks the native checker to trust an optimizer,
sampled equality, foreign-unit inverse, or new case-split instruction.

### Rational linear consequence

Fourier–Motzkin elimination combines a positive and negative coefficient row
with nonnegative rational weights to eliminate one coordinate. All retained
rows carry their weights in the original rows. Back-substitution proves the
projection exact; endpoints of finite rational bound intervals supply rational
witnesses. Eliminating every variable either gives such a witness or a row
`0<=beta` with beta<0 and a strict nonnegative infeasibility ray.

For an affine objective c+v*x, add an auxiliary mathematical coordinate y
equal to that objective and project onto y. A finite upper endpoint B is an
attained rational endpoint of a one-dimensional rational polyhedron. Its
retained multipliers produce `A^T*lambda=v` and `c+lambda^T*eta=B` after
dividing by the positive remaining y coefficient. The native proof only uses
those source-row multipliers, a constant and slack. The auxiliary coordinate
and its two defining rows do not survive into the returned proof.

This reconstructs both primal attainment and the precise dual certificate
needed here. It covers lower-dimensional sources and unbounded nuisance
coordinates. Assuming that the original source has a vertex would leave a gap.

### Unit retyping

Choose one path of factor k_v>0 from each ancestor v to u. Represent each
relevant coordinate x:v by its converted term X_x and retain the numerical
identity X_x=k_v*x. Different paths need not have coherent or reciprocal
factors; the explicit rational ratios reconcile them.

Conversion through addition and scaling is exact collected-form equality.
Conversion through min/max instead requires a lattice proof: convert the two
injections/projections for one direction, and scale the corresponding
inequalities for k_v*a,k_v*b by 1/k_v before converting for the reverse.
Only the resulting exact arithmetic identities are rewritten. Closed lets
unfold capture-avoidantly, and signed scaling transports both equality
directions by reversed negation followed by positive scaling.

The converted rows are logically equivalent to the reduct rows because every
path factor is positive. Each one also has a native proof from its original
row, including its normalized intercept. Numerical equivalence alone would
not provide the latter obligation.

### Route A: finite affine cells

Process nonlinear occurrences after their children. Each new comparison is
between affine representatives, so its two closed sign guards are affine.
Native lattice rules and the guard row certify the selected affine expression
in both directions. Live leaves have rational witnesses and ordinary affine
certificates; empty children have strict rational rays and are never admitted
as live source contexts.

At a live parent, guard discharge gives two common-query inequalities with
opposite positive-part penalties. F06's source-free weighted disjoint-hinge
proof removes them. If one child is empty, its ray must have positive guard
weight because the parent is feasible. Dividing gives a strictly stronger
version of the surviving guard, which can be grafted into the live proof.
Monotone native budget propagation preserves or improves its bound.

Do this in the original single-case contexts. After grafting converted rows,
localize the result, remove all global aggregation, and extend it into the
full context only as a local proof for the identical named case/rows. Recheck
the new fingerprint. Source-free query equalities may then be appended in
that scope. Only after every case has a proof of the same literal pair may
all_cases form the global conclusion. The F08 transfer tests enforce this
correction, including a new case where the proposed local bound is false.

### Route B: finite max-min certificates

Source-free native identities turn the difference into a finite max of finite
minima of affine leaves. The required translation, homogeneity, negation,
associativity and distributivity identities are derived rather than supplied
as opaque rewrites. The noncircular chain is:

    native lattice/arithmetic rules
      -> F06 source-free disjoint hinges
      -> finite generic positive-min proof
      -> closed typed substitution of that fixed lemma
      -> distributive max-min normal form
      -> lifted affine consequence and native clause proofs.

The generic positive-min proof only uses its fixed two-variable affine split;
it does not call U1 or ask a new nonlinear substituted guard to be affine.
This is where a superficially short completeness argument could be circular.

For each minimum clause, the lifted LP is feasible whenever the source case
is feasible. Its dual weights lambda>=0, alpha>=0 have sum(alpha)=1 and
`A^T*lambda=sum(alpha_j*a_j)`. Weighted native minimum projections compare
the clause to the alpha-weighted affine sum. Weighted source rows bound that
sum. No lifted LP variable is a native source premise.

If the dual is empty the clause is unbounded above. Otherwise a finite optimum
has a rational dual vertex: choose an optimizer with least positive support,
then use a supported kernel direction to contradict minimality unless those
columns are independent. There are finitely many possible supports. Combining
all vertex proofs by native meet, clauses by max_common, and cases by all_cases
gives the exact bound. This also proves U1 without a query-specific sign tree.

## 4. Why the optional results are stronger than pointwise existence

The max-min dual feasible sets depend on row directions and query leaves,
not their RHS. Retaining every vertex therefore yields one finite trace whose
replayed budget remains optimal at every admitted rational RHS revision (U11).
Every budget is recomputed from the current rows; no stale root is accepted.
The current transport adapter's choice of one meet parent is sound for its
current request but can remove a future optimum. The worked family exhibits
that loss, and 125 exact revisions have independent attaining models.

Withdrawal sets selected nonnegative dual coordinates to zero. That is a face,
whose vertices are exactly the old vertices satisfying those zeros. A complete
catalogue therefore remains complete for arbitrary withdrawals (U13). Absence
from an arbitrary supplied portfolio is not a proof of unboundedness. New rows
can introduce new joint information and need new arguments, as the x+y example
shows even when both old marginal certificates are replaced optimally.

Finite rational polyhedral unions admit explicit CPWA zero-set probes. They
separate any unequal projected reduct domains, including a nonconvex gap that
all affine upper-bound queries miss (U9/U10/U12). This is a useful information
characterization because the language's min/max operations can observe more
than the closed convex hull. The probes retain no empirical provenance by
themselves, and their violation magnitudes are representation-dependent.

A closed typed source substitution has a finite rational CPWA image. Its image
of the new reduct gives exact inclusion criteria for preserving and reflecting
old consequences (U16). Affine surjectivity is the unrestricted special case;
an injective diagonal map can add a false old correlation. A case-map adapter
is narrower than the global image theorem when one new case spans several
old cases.

For each native request, source-row-free quantitative deduction gives a finite
rational coefficient K against the characteristic violation term (U17).
The least nonnegative K is attained because its cellwise dual constraints form
a finite rational polyhedron projected onto K. This does not assume that a
ratio of two CPWA functions attains its supremum. A current certificate of
violation at most epsilon then gives budget b+K*epsilon after typed substitution.
The least global gain need not be sharp in one particular new context.

The report application (U14) holds only for the supplied mixture law. Its
rational least warranted report comes from the joint probability vertices;
the (0,1) zero-denominator corner must be treated separately and prevents every
strict report when present. Least warrant, robust-loss optimum and uniform
paired improvement are distinct objectives with explicit separating examples.

Finally, reflection through one conversion is characterized by a return path
or the absence of any feeding source (U15). Adding a hypothetical local
order-reflection rule alone still fails on the three pairwise source constraints
in 04e. Its function-space interpretation validates every proposed rule but
not the shared-coordinate conclusion. This is a rule invariant, deliberately
not a purported F05 countermodel of an actually valid full-source inequality.

The final [geometry refinement](04h_geometry_and_transfer.md) reconstructs U18
from a distance LP. Its finite dual vertices give a matrix-uniform violation
coefficient, with rational sharpness witnesses for a single case over arbitrary
feasible RHS. A weighted coordinate version retains the paired loss's individual
sensitivities. Zero sensitivity directions require a seminorm and LP attainment,
not a false compact-ball argument. This is a classical polyhedral error-bound
construction applied to the present source/transfer interface, not a novelty
claim. The two-row native example attains gain 1+2/e, and the report fixture
retains the sharper gain one instead of replacing all sensitivities by their
maximum. Current old bounds, matrix meanings and empirical interpretation
remain separate requirements.

### Final reconstruction checks

The unit-flow audit includes zero multiplication: it can erase a numerical
dependence but cannot change the unit of its proof premise. All children are
typed before collected-form cancellation. The full-source/reduct distinction
is also maintained for every negative example; a violating reduct point alone
is not labelled a refutation of the full source.

In affine source substitution, the dual offset cancellation uses the original
balance equation, and the reverse implication uses injectivity of M^T. Extra
new constraints cannot be omitted from the image condition. For quantitative
deduction, the proofs associated with each old case are first made unconditional;
only then can min_common combine their allowance expressions. This avoids
silently using all old cases as simultaneous source assumptions.

The native fixture receivers retain literal pairs as well as budgets and scope.
An initial extension fixture needed an explicit rewrite of a normalized row
back to x before requesting x; the unchanged receiver rejected the mismatch.
The saved report likewise distinguishes a single-case global portfolio from
a local request. Those were harness defects, repaired without weakening the
receiver or native inference rules.

## 5. Evidence limits and the task boundary

The universal results are the written constructions above and in 04–04f/04h.
The executable checks test finite supplied certificates, independently evaluated
rational countermodels, exact attaining models, context/request rejection and
retained proof alternatives. They do not infer a theorem from passing samples.
All emitted traces use the unchanged sixteen-rule kernel; the original F05,
F06 and F07 implementations are unchanged.

The existence predicate concerns finite mathematical derivations with adequate
resources. It is not a promise that Python's default recursion/memory limits,
an arbitrary producer cap, or a bounded search finds every proof. The current
fixtures do not implement a general LP solver, complete vertex enumerator,
max-min normalizer, CPWA image optimizer or minimal-gain solver. Those are
possible F11 design choices after the intervening tasks and gate.

F08's acceptance criterion permits an obstruction plus a constructive restricted
result. The one-way counterexample and U1 meet that substantive criterion;
the specification explicitly retains its unit-access restriction. U11–U18
are optional gains earned inside the protected work, not excuses to widen the
core claim to unrestricted completeness. No earlier accepted soundness result
is invalidated. F09 comparisons, F10's external contribution audit and Gate B
remain separate obligations. No global novelty, empirical proxy adequacy,
neural realization or unrestricted self-soundness claim is made here.
