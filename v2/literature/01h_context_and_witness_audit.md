# F03 — Variable contexts and existence of numerical witnesses

Session: 2026-09-24-S8 (America/Los_Angeles; clocks on September 25 UTC).
Base: `bbd54317f4d3dac2c6b96b06fae96dc29a504ea0`.
Status: source audit and finite specializations; not an adopted calculus or a
Gate A decision. Read with the [source register](F03_import_contracts.json)
and [previous source-rule reconstruction](01g_checked_source_derivations.md).

## 1. Two further source-use obligations

Two operations that look like harmless implementation details require evidence:

* Removing a variable absent from the conclusion can enlarge the allowed
  interpretations of a relational context.
* Introducing a number through optimality constraints does not by itself
  establish that those constraints have a model, or an attainable witness.

These are different issues: one changes the domain of a universal statement;
the other risks making that domain empty. Neither says that value-first
reasoning must keep all information or avoid optimization. The constructions
below identify explicit conditions and positive controls.

## 2. S10: a conclusion's free variables do not determine its context

**Source location.** Mio, Sarkis and Vignudelli, *Universal Quantitative Algebra
for Fuzzy Relations and Generalised Metric Spaces* (LMCS 2024), Definitions
3.5–3.6, Remark 3.7, and Definition 4.1(e). These define interpretations on a
whole related-variable space, not just the variables appearing in a term.
Remark 3.7 explicitly distinguishes the two domains. The finite construction
below is a specialization for this audit, not a quotation of its example.

### 2.1 A three-variable, two-value check

Let the variable context be X={x,z,y}, with the symmetric relation table

| d_X | x | z | y |
|---|---:|---:|---:|
| x | 0 | 1/2 | 1 |
| z | 1/2 | 0 | 1/2 |
| y | 1 | 1/2 | 0 |

Let the target be A={0,1} with d_A(a,b)=0 for a=b and 1 otherwise. There are no
operation symbols. An admitted interpretation tau:X->A must satisfy

    d_A(tau(i),tau(j)) <= d_X(i,j)  for every ordered pair i,j.

The x,z bound forces tau(x)=tau(z): the only target distance below one is zero.
The z,y bound likewise forces tau(z)=tau(y). There are exactly two admitted
interpretations, the two constant maps. Consequently the target A satisfies

    forall (X,d_X). x = y.

Now delete z because it does not occur in the displayed conclusion. On
Y={x,y}, the restricted context permits all four assignments; its off-diagonal
bound is one. The assignment x=0,y=1 refutes

    forall (Y,d_X|Y). x = y.

Both interpretation sets are nonempty. All quantities are finite. The
counterexample does not rely on a missing triangle law: both displayed spaces
are ordinary metric spaces. The lost information is the possibility of extending
an endpoint assignment to the intermediate variable in the specified target.

### 2.2 Exactly which direction is safe?

For a fixed nonempty target algebra A, define

    R : Hom(X,A) -> Hom(Y,A),  R(tau)=tau|Y,

where Hom here means the relation-preserving interpretations, not an invented
new model representation. Every full interpretation restricts to a permitted
smaller one. Therefore validity on Y implies validity on X for conclusions
using only Y. The reverse is guaranteed when R is onto: every smaller
interpretation can then be extended, and evaluating a term on Y is unchanged.

Surjectivity is sufficient for every such conclusion; a particular conclusion
can survive even when R is not onto. We do not claim that every failure of
surjectivity is distinguishable by this language's equations.

There is also a useful simple elimination rule. If one extra variable z has
all incoming, outgoing **and diagonal** bounds equal to one, any interpretation
of Y extends by choosing an arbitrary target element for z. The target must
be nonempty. Keeping a diagonal zero is not the same premise in a general fuzzy
relation: a nonempty target need not contain an element with zero self-relation.
For example a one-point target with d(a,a)=1/2 admits an unconstrained empty
context but no assignment to a variable whose diagonal is required to be zero.

**Consequence for an eventual compiler.** Syntactic dead-variable elimination
is not licensed on relational contexts by its usual justification for ordinary
terms. Preserve the context, prove the needed extension property, or explicitly
accept a stronger, more restrictive judgment and justify it separately. No efficient general extension
test is established here. Existing F03-C46 substitution side conditions remain
necessary; this observation does not replace them.

## 3. S12: a finite optimum certificate requires an existing witness

**Source location.** Bacci, Mardare, Panangaden and Plotkin, *Rational Lawvere
Logic* (CSL 2026), §5, “Kantorovich distance.” Its proposed premises constrain a
coupling, finite nonnegative dual potentials, and an atom K between the dual
and primal objectives in the reversed direction to weak duality. Read these
as an optimality-certificate interface. The following is a direct audit of its
satisfiability boundary, not a challenge to arithmetic soundness or the finite
completeness theorem.

### 3.1 What the premises force when a model exists

For probabilities mu,nu on a finite set, let a feasible coupling be pi, a
feasible finite potential be F, and write

    C = sum_ij pi_ij d_ij,
    D = |sum_i F_i mu_i - sum_i F_i nu_i|.

Potential feasibility and the coupling equations imply weak duality D<=C.
The source's two additional sequent premises impose D>=K and K>=C. Hence any
model of all the premises has D=K=C. This statement is conditional on existence.
It does not produce a coupling, a potential, or their finite attainment.
The objects here are source-certificate witnesses, not a policy available to
an agent before it observes its situation.

### 3.2 A minimal infinite-distance obstruction

Use two points 0,1, mu concentrated at 0 and nu concentrated at 1, with

    d(0,0)=d(1,1)=0,  d(0,1)=d(1,0)=infinity.

The marginal conditions force pi_01=1. Thus C=infinity. Every permitted finite
F has finite D=|F_0-F_1|, so D>=K>=C is impossible. The displayed optimality
premises have **no model** for this input. Yet the transport distance is
well-defined as infinity, and the supremum of feasible finite dual objectives
is infinity. A supremum need not be achieved by a finite witness.

Accordingly, “every model assigns K the desired value” is not enough to use K
as a satisfiable definition. This is an **existence restriction on the imported
certificate interface**, not a counterexample to the conditional implication
that its models are optimal. No current project result relied on existence for
this input. The source permits extended distances; our explicit input shows why
that allowance alone does not supply a finite potential certificate.

Positive control: replace the off-diagonal distance by any finite d>=0. The
same coupling, F=(d,0), K=d satisfies all the displayed conditions. No uniform
upper bound across the family of finite d is needed. Thus distinguishing a
finite value from the infinity endpoint preserves genuinely unbounded examples.

### 3.3 A structural finite-coupling criterion

For a finite extended pseudometric, define i~j iff d_ij is finite. Reflexivity,
symmetry and the triangle inequality make this an equivalence relation. A
finite-cost coupling exists exactly when mu(C)=nu(C) for every component C.

Necessity: any positive coupling mass across different components has infinite
cost. A finite-cost coupling therefore moves all mass within components, and
the row and column constraints give equality of their masses.

Sufficiency: in a component of common mass m>0, set

    pi_ij = mu_i nu_j / m  (i,j in C),

and set all cross-component and zero-mass-component entries to zero. Direct
summation gives the required marginals. Every positive term has finite d_ij,
and there are finitely many terms, so the total cost is finite.

This establishes existence of a finite *primal* witness. It does not claim the
constructed product coupling is optimal. General dual attainment additionally
uses the appropriate finite optimization theorem. Our two-point positive
control exhibits primal and dual witnesses directly, without that extra import.

**Register disposition B-S12-KR-01.** Do not assume that the §5 optimality
premises are satisfiable for every extended-metric input. Admit them only with
witness/existence evidence or use a separate approximation/endpoint interface.
A feasible potential and coupling can instead be kept as separate lower and
upper bounds; optimality need not be assumed merely to use those bounds.
The guarded arithmetic results and earlier finite certificates are unchanged.
This is a same-agent source-adapter finding, not an author-confirmed erratum.

## 4. Reading closure, not a new phase

The session rechecked S12's finite/polynomial consequence interface and its
fresh-variable and endpoint conditions; S10's distinction between equality,
relation bounds and the full context; and S13's original signed language and
component polarity. Source locators and failed image requests are recorded in
the session/source manifest. The bibliography is unchanged. Previously
ambiguous stronger source sentences remain unused, not silently repaired.

For downstream work the obligations are now explicit: preserve a context or
justify its elimination; preserve a source guard or prove its premise; and
separate a numerical optimum from an existing witness. These complement, rather
than supersede, the already checked local derivations. None selects a permanent
carrier, provides a complete source prover, or advances F04.

## 5. Executable evidence

The [finite checks](../checks/f03_context_witness.py) enumerate the small
interpretation spaces and verify the explicit coupling constructions with exact
rational arithmetic. The general arguments above are not inferred from finite
tests. The infinity obstruction is handled symbolically as a component-mass
obstruction, not by substituting a large floating-point number.

The [report](../checks/F03_context_witness_results.json) is deterministic. These
are source-boundary regression fixtures, not a held-out experiment or a general
optimizer. The [work log](../work_logs/F03_2026-09-24_S8.md) determines task status
and measured effort.

## Source links

S10: [LMCS journal version](https://lmcs.episciences.org/14876/pdf),
Definitions 3.5–3.6, Remark 3.7, Definition 4.1, Theorem 4.4 and Lemmas 5.3–5.8.
S12: [official CSL 2026 text](https://drops.dagstuhl.de/storage/00lipics/lipics-vol363-csl2026/html/LIPIcs.CSL.2026.3/LIPIcs.CSL.2026.3.html),
Section 5, Kantorovich distance; the finite guard/completeness interfaces remain
those separately recorded in the source register. These source locations support
the interfaces; the finite countermodels and component construction are worked
arguments in this note.
