# F03 — Checked source derivations and final import boundaries

Session: 2026-09-24-S7 (local research date; UTC readings may be September 25).
Base: `e1454a87801266b10b602f5babd737f5eabbb6df`.
Scope: F03 source audit only. This note does not select a calculus, perform F04,
or implement a complete external proof system. Task completion is determined
by the work record, not by this note's existence.

Source identifiers refer to [F03_sources.json](F03_sources.json). Earlier
inspections and objections remain historical records. The goal here is to turn
selected source interfaces into actual small derivations that can be checked
line by line. Original adapters are distinguished from quoted source results.

## 1. S12: an explicit directed-loss derivation

Locator: Bacci–Mardare–Panangaden–Plotkin, *Rational Lawvere Logic*, CSL 2026,
[official paper](https://doi.org/10.4230/LIPIcs.CSL.2026.3), sections 3–5,
Table 2 (printed 3:8), and the worked distance derivation on printed 3:9.

**Source interface.** Write `a => b` for the source formula `a multimap b`,
not for entailment. Its value is `(b-a)_+`, with the source endpoint conventions.
Write `+` for its additive connective. A sequent `a,b |- c` means `a+b >= c`.
The derivation below uses identity, permutation, cut, and the reversible
premise-merging and additive-adjunction rules. Hypotheses remain a set of
sequents; numerical antecedents remain lists. No contraction is used.

**Reconstruction.** Let `u=(y=>x)`, `v=(z=>y)`. These names abbreviate formulas,
not new assertions or an optimization over possible models.

| Line | Sequent | Justification |
|---|---|---|
| 1 | `u |- y=>x` | Identity, after expanding `u`. |
| 2 | `u+y |- x` | Reverse additive adjunction on line 1. |
| 3 | `u,y |- x` | Expand the additive antecedent. |
| 4 | `v |- z=>y` | Identity, after expanding `v`. |
| 5 | `v+z |- y` | Reverse additive adjunction on line 4. |
| 6 | `v,z |- y` | Expand the additive antecedent. |
| 7 | `v,z,u |- x` | Cut line 6 into the occurrence of `y` in line 3. |
| 8 | `(u+v)+z |- x` | Permute and merge antecedents. |
| 9 | `u+v |- z=>x` | Forward additive adjunction. |

From extra hypotheses `r |- u` and `s |- v`, expand line 9, substitute each
hypothesis using cut, and merge again. The resulting conclusion is

```
r+s |- z=>x.
```

Under value-oriented names `x=V(M)`, `y=V(N)`, `z=V(P)`, the formula `y=>x`
measures the loss of replacing M with N, not the reverse. The result composes
two declared error allowances. This is a reconstruction of a source-rule
instance, not a novel triangle inequality. All endpoint cases follow the
source interpretation; a finite useful allowance is an additional requirement.
No choice of a policy, factual calibration of V, or observation of a hidden
state follows from this arithmetic derivation.

## 2. Finite signed coordinates: where cancellation enters

The existing pair adapter represents a finite real value as `x=x+ - x-`,
with nonnegative finite coordinates. These are coordinates, not a presumption
that values themselves cannot be negative. There is no common magnitude cap.

Let the two replacement bounds be `x-y <= r` and `y-z <= s`, with nonnegative
r and s. Their nonnegative source sequents are

```
y+ + x- + r |- x+ + y-
z+ + y- + s |- y+ + z-.
```

The source rules derive addition of inequalities: from `A |- B` and `C |- D`,
start with identity on `B+D`, expand its antecedent into `B,D`, and cut A and C
into those two occurrences. Merging produces `A+C |- B+D`. Applying this to
the displayed premises and rearranging yields

```
(z+ + x- + r + s) + (y+ + y-) |- (x+ + z-) + (y+ + y-).
```

The source cancellation rule additionally requires `|- |y+ + y-|`.
With this finiteness guard the conclusion is

```
z+ + x- + r + s |- x+ + z-,
```

which decodes exactly to `x-z <= r+s`. The guard is true for the stated finite
coordinate interpretation; a proof-producing adapter must supply its proof
or retain it as an explicit premise. This record does not pretend that a
semantic finiteness argument has already been emitted by a program.

The cancellation premise is essential. With a common summand of infinity,
`0+infinity |- 1+infinity` is satisfied, whereas `0 |- 1` is not. Infinity is
not an arbitrarily large finite coordinate. The pair adapter therefore applies
to real values unbounded across inputs, not unrestricted `infinity-infinity`.

This separates two usable routes: direct nonnegative directed losses, and
nonnegative coordinate proofs about signed values. Neither route fixes the
project's eventual primitive carrier.

## 3. Source proof audit: polynomial completeness versus a concrete certificate

S12's Theorem 11 quantifies over a finite polynomial sequent problem and a set
of finiteness guards covering variables in both premises and conclusion. The
proof on printed 3:15–3:16 invokes its Theorem 13, then uses Lemma 14 to express
polynomials with signed coefficients through nonnegative formula values. This
is the eligible source theorem, rather than an automatic completeness claim
for arbitrary KL or operational syntax.

Here is the algebraic check behind the cited certificate, with names chosen
for this audit. Let the desired finite polynomial inequality be `f >= 0` on a
feasible set W. Suppose a certificate gives polynomials a,b nonnegative on W
and a nonnegative integer k with the identity

```
a f = f^(2k) + b.
```

At a point of W where f were negative, the left side would be nonpositive and
the right side strictly positive (also when k=0). Thus the certificate proves
the desired inequality. Checking that identity and nonnegativity of a,b uses
only its stated generators; discovering a certificate is a different problem.

The source proof translates this into two branches. If a is positive, finite
multiplicative cancellation is legitimate. If a is zero, k=0 is inconsistent,
and k>0 forces the even power to zero; repeated zero-product reasoning then
forces f to zero. The source does not infer a uniform positive lower bound on
a from its pointwise positivity. Nor does a small numerical residual in the
polynomial identity certify exact equality.

For the existing finite signed-coordinate translation, the correspondence of
assignments is already proved: every real assignment has finite nonnegative
representatives, and every admissible pair assignment decodes to a real one.
The guards exclude infinite coordinates, not arbitrarily large finite values.
S12's certificate route therefore remains available for this translated
polynomial problem. It does not cover a variable logarithm or supply a common
policy witness. The present tests still do not implement certificate search.

**Boundary retained.** The printed/parsed Phase 5 Stage 2 uses truth labels for
`0 |- 1` and `1 |- 0` opposite to section 3's displayed sequent interpretation.
This audit does not need that normalization stage: its examples use the explicit
rules or the directly polynomial guarded interface. This is a located source
wording issue, not an author-confirmed erratum or a rejection of Theorem 11.
No unavailable page image is reported as inspected.

## 4. S10: why a substitution must carry a relation proof

Locator: Mio–Sarkis–Vignudelli, *Universal Quantitative Algebra for Fuzzy Relations
and Generalised Metric Spaces*, [LMCS 20(4:19), 2024](https://lmcs.episciences.org/14876),
Definition 4.1(e,f,h), Theorem 4.4, and Lemmas 5.3 and 5.8.

**Source interface.** A variable context supplies a relation `d_X:X^2 -> [0,1]`.
Assignments must respect every entry. Substituting terms for variables requires
proofs of those same entries for the substituted terms. Ordinary equality and
zero relation are different judgments. The source's infimum rule is infinitary;
its completeness is not a finitary certificate-search theorem.

### 4.1 A concrete instance with all side premises shown

Take X={x,y} with `d_X(x,y)=1/4` and the other three entries equal to 1.
The source variable rule supplies the judgment `forall X. x =_(1/4) y`.
For a target context Y and a substitution `sigma(x)=t`, `sigma(y)=u`, the
substitution premise set has four members:

```
forall Y. t =_1 t
forall Y. t =_(1/4) u
forall Y. u =_1 t
forall Y. u =_1 u.
```

The three bound-1 premises are automatic by the maximum-bound rule. The
quarter-bound premise is not. A proof of it, followed by substitution and cut,
licenses the desired instance. This remains true when t or u contains an
amplifying operation: it is the actual substituted terms, not just the original
variables, whose relation needs checking.

For a semantic check use real values with `d(a,b)=min(1,max(a-b,0))` and a unary
operation `double(a)=2a`. This is a legitimate fuzzy-relation algebra in the
source's general setting; global operation nonexpansiveness is not assumed.
From `d(a,b)<=1/4` alone, replacing x,y by double(a),double(b) is not licensed:
a=1/4,b=0 gives a relation of 1/2. Tightening the input premise to `d(a,b)<=1/8`
suffices for this concrete double operation. That is a separately checked
operation law, not a free consequence of its name or of the source framework.

Diagonal entries of 1 were intentional. Replacing them by zero would restrict
the admitted assignments in an arbitrary fuzzy-relation algebra, because its
relation need not be reflexive. Likewise, a triangle law must be included in
the selected relational theory; it is not present just because the relation is
numerical. This is a precise input contract, not a reason to exclude directed
relations or unbounded value carriers.

### 4.2 The soundness argument identifies the exact obligation

Given an allowed target valuation tau, form a source valuation by evaluating
each substituted term: `hat_sigma(x)=eval_tau(sigma(x))`. The four side
premises above make this a relation-preserving map from X. Only then can the
original universally quantified judgment be applied. Structural evaluation
commutes with term substitution, yielding the required target judgment.
The same construction works for larger contexts with one side premise for
each ordered pair of variables.

A useful distinction follows. An operation can fail to preserve the source
context globally, yet a particular substitution through it can be valid when
stronger input premises certify its outputs. Conversely, unrestricted source
operations do not mean unrestricted logical substitution. This is the part of
Theorem 4.4's argument the proposed value bridge must retain.

### 4.3 Why the free-model result does not remove the obligation

The source constructs term classes using provable ordinary equality. Its
relation between classes is the infimum of provable bounds. Lemma 5.3 identifies
that infimum with a provable bound using the order-completeness rule; Lemma 5.8
then supplies every substitution side premise before concluding that the free
model satisfies the axioms. A finite implementation omitting the infimum rule
can still check its finite derivations, but cannot simply claim this entire
completeness proof. Our explicit four-premise instance needs no infinitary step.

## 5. S13: a signed source changes the structural rules, not just the range

Locator: Metcalfe–Olivetti–Gabbay, *Sequent and Hypersequent Calculi for Abelian
and Lukasiewicz Logics*, arXiv:cs/0211021v1 (November 18, 2002), Definitions
10–12 and 29–30, Theorems 32 and 39, and the two admissible cut rules immediately
after Theorem 39 (PDF indices 4–5 and 8–11). These locators are for the inspected
preprint, not for a differently paginated publication.

**Source reconstruction.** In its real characteristic algebra, a component
`Gamma |- Delta` means `sum(Gamma) <= sum(Delta)`. A hypersequent asks that at
least one component hold in each valuation. This component polarity is opposite
to the RLL convention used above. Antecedents and consequents are multisets,
not idempotent sets. Empty sums are zero. Its additive group permits negative
values and ordinary finite cancellation.

For example, express the signed replacement assumptions in this convention as

```
x |- y,r       and       y |- z,s.
```

The source's admissible cut yields `x |- r,z,s`, which expresses `x-z <= r+s`.
No infinity guard is needed because the characteristic algebra is the finite
real line. This is an application of the displayed admissible rule; we do not
infer unrestricted local-hypothesis completeness merely from a theorem about
valid hypersequents. The source's Theorem 39 is a validity completeness result
for its actual language and rules.

The source's atomic validity certificate in Proposition 37 balances the
multiplicities of every atom on the two sides using nonnegative integer
weights, not all zero. For the two components `x |- y` and `y |- x`, weights
(1,1) balance the atoms. This proves that at least one comparison holds under
every real assignment, not that one component is valid under every assignment.
That distinction is precisely the per-model versus common-witness issue in
our earlier operational examples.

**Why retaining the RLL rules on signed formula values fails.** In RLL,
weakening takes `0 |- 0` to `0,a |- 0`. Its soundness uses `a >= 0`. Assigning
`a=-1` makes the latter inequality false. Consequently, extending the value
range to the real line while retaining all RLL rules unchanged is not a sound
bridge. This is a local structural-rule obstruction, not a prohibition on
signed values. The finite-pair translation leaves source formulas nonnegative;
the Abelian route uses different structural rules; and the directed-loss route
keeps losses nonnegative while allowing the represented values to be signed.

In Abelian polarity, unrestricted internal antecedent weakening would also
fail, now by adding a positive value to `0 |- 0`. Its *external* weakening adds
a hypersequent alternative and has a different meaning. Neither source permits
silently moving a weakening rule from one level or polarity to the other.
The Abelian signature inspected here does not by itself contain arbitrary
polynomial multiplication or logarithms. Its characteristic-algebra results
cannot be promoted to such extensions without a further argument.

## 6. What is checked and what remains external

This audit distinguishes three steps: a formula translation, a finite
source-rule derivation, and a claim about the operational evidence represented
by its premises. Only the first two can be discharged by manipulating the
finite source syntax. A loss bound for a real model, a KL support condition,
or a common feasible policy must enter as an independently justified premise.
An arithmetic proof does not manufacture any of them.

The guarded signed-pair and direct-loss derivations above are small source
instances. They do not require a new source bibliography, a global bound on
finite real values, a proof search algorithm, or the entire RLL completeness
argument. They also do not choose among S/P/T/G. A checked derivation is useful
precisely because its external premises and its limited rule set can be listed.

### 6.1 Arithmetic residuals versus an abstract distance name

S12 section 5 also explains a translation of finitary quantitative equations by
introducing propositional names for the distances between terms. This is not
the claim that every collection of nonnegative formula values automatically
satisfies every distance law. The chosen equations or inference axioms must
also enter the translated theory. In contrast, section 1's residual formulas
are built from source implication, so their displayed chain is derivable from
its arithmetic rules alone. The external interpretation of the values still
needs justification.

This resolves a potential ambiguity in the proposed KL bridge. A KL penalty
may be an input term in an objective; it does not thereby become an abstract
metric that inherits a triangle rule. The earlier KL counterexample is not
retracted. Bounds on differences of *total finite objective values* can be
chained by the signed or residual routes above without asserting a KL triangle
inequality. Which empirical or analytic premises establish the component
bounds remains outside this arithmetic certificate.

### 6.2 Actual finite certificates and their limits

The [audit module](../checks/f03_checked_derivations.py) emits and checks the two
finite derivations in sections 1 and 2. Its separate validator checks the
advertised goal, predecessor references, exact formula syntax, multiplicities,
and the cancellation guard. Positioned cut/premise rules and a whole
permutation stand for their finite source-permutation expansions. Reassociation
of addition is emitted through identity, premise unfolding/folding and
permutation, not accepted because a floating-point evaluation happens to agree.

The [machine-readable report](../checks/F03_checked_derivations_results.json)
retains every node and every explicit assumption. Changing an assumption in a
certificate also changes its conditional theorem: accepting an explicitly
assumed guard does not prove that a real model meets it. Inconsistent assumptions
can give a vacuous valid conclusion, so premise satisfiability is not claimed.

The validator checks no multiplication/division rules, disjunctive branch
reasoning, source completeness theorem, logarithm law, policy synthesis or
operational evidence. It is an audit fixture, not F11's proposed reasoner.
The 18 tests include deliberately damaged certificates, an extended-value
arithmetic grid, and finite signed coordinates at very large magnitudes.
They test this implementation and these certificates; the source-rule
soundness argument remains the justification for unenumerated valuations.

**Review boundary.** Rule schemas and derivations were checked by the same agent
against the source text. This is not independent verification or a proof-assistant
formalization. A later adopted calculus must still state its own signature and
prove that the translation preserves its intended consequence relation.
