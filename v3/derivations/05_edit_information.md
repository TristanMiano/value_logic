# P3-05 — Information that survives repeated edits

Contributor: **ChatGPT (GPT-6 Astra Pro)**. October 8, 2026 UTC.
Status: **S3 finite derivation complete**, ordinary reconstructions and scoped adapters.
Read with the [portfolio construction](05_portfolio_transport.md) and
[primary comparisons](../literature/05_portfolio_sources.md).

## 1. The information state is not the hidden world

Let S be a finite, explicitly constructed collection of **observable record
versions**. Each version may itself describe many unresolved mathematical or
hypothetical cases. A named edit e acts by a supplied deterministic total map
$`T_e:S\to S`$. An inadmissible edit may lead to an explicit failure state;
it does not acquire a favorable loss by becoming undefined.

A service can request an exact numerical/status output o(s), or some action
from a supplied nonempty acceptable set A(s). For the application, one choice
is the set of actions with a verified uniform regret tolerance over the
nonempty selected cases of version s. Establishing that set is a separate
computation and premise obligation. No hidden truth answer or full arithmetic
model is supplied by the finite graph. Records, evaluation and graph
construction cost work.

A self-contained summary machine has a finite code c, a displayed answer
depending only on c, and updates c using the named edit. It receives no free
old record, unbounded readable history, clock phase or uncharged side channel.
Changing that access contract can change every minimum-state statement below.
These are scoped information conditions, not a mandatory representation of
all values or of the entire agent.

## 2. Exact values: a familiar stable quotient

Define

```math
s\equiv t\quad\Longleftrightarrow\quad
 o(T_w s)=o(T_w t)\text{ for every finite edit word }w.
```

The empty word compares current outputs. Composition applies edits in their
written order. Costs or resource observations can be added to the requested
output trace; they are not automatically preserved by numerical equality.

**CT05-9 (ordinary output congruence).** The relation is an equivalence,
preserves o, and obeys $`s\equiv t\Rightarrow T_e s\equiv T_e t`$.
It is the coarsest equivalence with these properties. Consequently the
quotient is sufficient for every future exact requested output, and any
stationary functional recoding with the same self-contained contract must
separate distinct classes.

**Proof.** Equality of all continuation outputs gives reflexivity, symmetry
and transitivity. Prefixing e to every continuation proves edit stability.
For any other stable output-preserving equivalence, induction on word length
preserves the related states and their outputs, proving containment in this
one. The quotient update is therefore well-defined, while a decoder receiving
one code cannot return two distinct required continuation outputs.

Starting with current-output classes, repeatedly split classes by the tuple
of successor classes for every edit. Each strict round adds a class, so with
N states and k initial classes there are at most N-k strict rounds. The
fixed partition has exactly the above properties. A finite distinguishing
word for each separated pair plus a closure check provides independently
checkable sufficiency and separation evidence. This is automata minimization
applied to task records, not a new general minimization theorem.

Current-output agreement is weaker. For a three-bit record (a,b,c), output a,
and edit $`(a,b,c)\mapsto(b,c,0)`$, records 000 and 001 agree now and after
one edit, but disagree after two. With only an identity edit, b and c can be
forgotten. Adding the shift can require retaining them. A declared bijective
renaming must transport the edit table too; merely renaming outputs is not
an operational equivalence.

## 3. Some good action: equality is unnecessarily strong

For a canonical, stationary map q(s), a code class C needs

```math
\bigcap_{s\in C}A(s)\ne\varnothing,
\qquad q(T_e s)=q(T_e t)\text{ whenever }q(s)=q(t).
```

**CT05-10 (action-compatible partition).** These conditions are necessary and
sufficient for a self-contained deterministic quotient whose output is some
acceptable action at every version. Choose one action in each intersection
and the common successor code; necessity follows from the one output and one
update available at that code. This preserves the selected action service,
not the entire action set, every tie, absolute values or a prescribed tie rule.

There need not be a unique coarsest such partition. With identity edits and
$`A_1=\{a,b\}, A_2=\{b,c\}, A_3=\{a,c\}`$, every pair can share a code,
but all three cannot. Several incomparable two-class partitions work.
Pairwise compatibility alone does not establish a common action for a class.
The output contract of ordinary incompletely specified binary machines must
not be imported without checking this distinction.

With identity edits, the minimum number of codes equals the minimum number
of actions whose acceptability sets cover S. One direction reads the action
of each code; the other assigns every state to an acceptable chosen action.
This is a direct set-cover characterization, not a new efficient solver or a
claim that all probability information must survive.

## 4. A relation can need less memory than a canonical recoding

The requirement that each semantic record always have the same code is an
extra restriction. Permit instead an invariant $`s\in C_i`$, where nonempty
sets C_i may overlap. A record reached through different histories may have
different valid codes. The agent still reads only its actual code; it does
not secretly inspect which s in its current class occurs.

**CT05-11 (ordinary closed-cover adapter for decisions).** Such a deterministic
summary machine is possible with codes i exactly when there is a cover
$`\bigcup_i C_i=S`$, actions $`a_i\in\bigcap_{s\in C_i}A(s)`$, and a transition
choice j(i,e) satisfying

```math
 T_e(C_i)\subseteq C_{j(i,e)}.
```

Initial encoding chooses any containing class with a declared tie rule.
The cover invariant is preserved by induction. The selected action therefore
remains acceptable after every edit sequence. Conversely, for any such finite
machine, let C_i collect the semantic records compatible with code i over
all admitted initial states and histories. Correctness and deterministic
updates give the intersection and closure conditions. Empty/unreachable codes
may be removed. This is the established closed-cover idea with the task's
arbitrary action sets and evidence semantics made explicit.

### A strict three-record separator

Use loss tables (action a, action b) at records 1, 2, 3:

```text
1: (0,1)     2: (0,0)     3: (1,0)
right: (1,2,3) -> (2,3,3)
left:  (1,2,3) -> (1,1,2)
```

Thus A1={a}, A2={a,b}, A3={b}. The two overlapping classes
C_a={1,2}, C_b={2,3} suffice. Every right edit sends either code to C_b;
every left edit sends either code to C_a. The code's action is a or b.
A single code is impossible because records 1 and 3 have no common action.

No two-class **partition quotient** works. The only possible merger is {1,2}
or {2,3}. Right splits the successors of the first merger; left splits the
second. The merger {1,3} has no common action. Thus two relational codes
suffice where a canonical quotient needs three. All actions here are optimal
for their given finite loss tables; no probability law is required.

For exact outputs rather than permissible actions, overlaps cannot beat the
number of CT05-9 classes: states within one cover class must agree after every
continuation by closure and exact output, so each cover class lies within a
Nerode class. Each distinct class needs coverage. This explains why exact
numerical recovery and action-only retention have different state costs.

## 5. Scope, checking and resource meaning

This finite-memory distinction is not a claim of a new logical learner. It
addresses I01/V02/R01: what an operational representation must preserve when
future edits are part of the consumer contract. The proof portfolio concerns
hidden case-dependent **proof choice for one fixed action comparison**;
the closed-cover machine concerns **observable version-dependent action
choice using a readable code**. Confusing the two would introduce forbidden
hidden information.

A sound graph certificate must bind the complete state records, outputs or
acceptable sets, edit names, successor table, and any preserved edge labels.
Equality of a table hash alone does not establish the source graph's semantic
adequacy. The executable adapter checks a supplied graph, not the correctness
of arbitrary external programs used to generate it. A worked finite premise
version graph is built separately from explicit Boolean source evaluation.

Compression does not imply lower total cost. The graph may be much larger
than one current query, minimization costs computation, and storing the cover
incidence relation for validation can exceed the compact online code. The
transition/output table must remain available. Report graph construction,
certificate checking, storage and online lookup separately. Ordinary finite
state minimizers and dependency-aware solvers may use the same construction.
A query family admitting no acceptable action must retain a named failure or
fallback service; these theorems do not manufacture a good action.
