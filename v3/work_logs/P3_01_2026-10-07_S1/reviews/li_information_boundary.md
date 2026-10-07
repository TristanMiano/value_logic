# P3-01: Logical Induction and finite checked information

Reviewer: **GPT-6 Astra Pro**, `/root/p301_induction_sources`.
Date: **2026-10-07 UTC**. Same-model internal, nonblind review.
Scope: operational comparison and elementary separating constructions for
P3-01. No later task, canonical edit, theorem-priority claim or gate decision.

**Disposition:** a finite Boolean constraint engine can implement the exact
finite restriction of Logical Induction's current assessment worlds when it
includes every relevant prime atom and actually completes the computation.
A bounded partial record usually supplies a weaker approximation. Neither
exact finite evidence coherence nor fixed-query eventual correctness implies
the Logical Induction criterion. Conversely, Logical Induction does not require
exact coherence with the admitted record on every finite day.

## 1. Five primary-source contracts

Primary paper: Garrabrant, Benson-Tilsen, Critch, Soares and Taylor,
[*Logical Induction*](https://intelligence.org/files/LogicalInduction.pdf).
Page numbers below are printed page numbers, not zero-based PDF indices.
These compact contracts are the source-derived summary; subsequent
constructions and interface checks are this review's own analysis.

1. **Representation:** markets are computable rational pricings; belief states
   additionally have finite support and default zero. Definitions 3.1.2–5,
   pp. 14–15.
2. **Disclosure:** a deductive process is a computable nested sequence of finite
   sets. Its bare definition requires neither consistency nor soundness.
   `Gamma`-completeness means `PC(D_infinity)=PC(Gamma)`. Definitions 3.2.1, 3.2.4,
   pp. 15–16.
3. **Worlds:** `PC(D_n)` contains Boolean-compositional worlds satisfying `D_n`.
   First-order prime sentences include quantified sentences; first-order axioms
   must be supplied separately. Section 2, pp. 12–13; Definition 3.2.3 and
   footnote 1, p. 16.
4. **Exploitation:** polynomial-in-unary-`n` traders generate continuous,
   expressible portfolios. Cumulative holdings, assessed over current
   `PC(D_n)`, must be bounded below and unbounded above. Sections 3.3–3.5,
   especially Definitions 3.3.1, 3.4.3, 3.5.1, pp. 16–20.
5. **Properties:** Section 4 assumes consistent computably enumerable `Gamma`
   and `Gamma`-complete disclosure; §§4.8–12 add computable-function
   representation. Theorems 4.1.1–2, 4.2.1 and 4.6.1 give convergence,
   limit coherence, theorem-sequence learning and finite-perturbation closure.
   Assumptions p. 22; results pp. 22–24, 36.

## 2. Our finite operational reconstruction

Fix one theory/checker/interpretation version. Let `D_t` be the finite record
whose sentences are treated as hard evidence. Let `A_t` contain **every prime
sentence** occurring in `D_t` and in the finitely many formulas currently being
queried. Parse only the Boolean structure around these primes. Define

$$
V_t=\{v\in\{0,1\}^{A_t}:v\models D_t\}.
$$

Then the exact projection identity is

$$
V_t=\{W|_{A_t}:W\in\mathrm{PC}(D_t)\}.
$$

The forward inclusion follows by restriction. For the reverse inclusion,
extend a satisfying `v` arbitrarily to every remaining prime sentence, and
evaluate all formulas by their Boolean structure. Because every prime used by
`D_t` lies in `A_t`, the extension still satisfies `D_t`. This proves the identity
without an oracle for models of the full theory. Quantifier instantiation is
not obtained by opening a quantified prime: a needed relation must be present
in, or derived into, the checked record.

The identity specifies a mathematical target, not a free implementation.
Enumerating all assignments takes `2^|A_t|` candidates before formula-evaluation
costs. An implementation may cap its domain or use a sound solver, but must
charge parsing, inference, search, storage and projection, and say which result
was actually certified. A stopped enumeration is not a completed enumeration.
Soundly overapproximating possible worlds and listing only some found worlds
are different operations; the latter need not support an upper loss bound.

If the active constraints `C_t` omit some of `D_t`, or are only selected
consequences of `D_t`, the resulting world set can overapproximate the current
record. Projecting onto fewer atoms requires eliminating omitted atoms, not
simply dropping every clause mentioning them. The next witness makes that
distinction explicit.

### Witness 1: dropping mixed clauses is not exact projection

Take

$$
D=\{u\lor z,\;u\lor\neg z\}.
$$

Every satisfying assignment has `u=1`: `u=0` would require both `z=1` and
`z=0`. Hence the exact projection onto `{u}` is `{1}`. If both mixed clauses
are dropped and no replacement is derived, the retained constraint set is
empty and admits both values of `u`. The latter is a sound outer approximation
of this projection, with weaker conclusions; it is not the same information
state. Deriving `u` by resolution or eliminating `z` is real work to record.

This finite Boolean check is complete by the two possible values of `u`.
It establishes no complexity advantage or new logical-uncertainty theorem.

## 3. Two directions that fail

For this section, “exact current coherence” means that every current formula
price is the probability of that formula under a distribution supported on
`PC(D_n)`. For a finite interface the analogous condition concerns its declared
formula domain. It is stronger than merely keeping individual prices in
`[0,1]` or assigning price one to explicitly stored theorems.

### Witness 2: exact coherence and fixed-query learning still do not imply LI

Use propositional atoms `A_1,A_2,...`, with an effective encoding in which
`n -> A_n` is polynomial-time in unary `n`. Define

$$
\Gamma=\{A_k:k\ge1\},\qquad
D_n=\{A_k:2^k\le n\}.
$$

This is a computable nested finite disclosure process for a consistent theory,
and its union is exactly `Gamma`. At day `n`, give every disclosed atom value
one; give the undisclosed atoms independent fair Boolean values. Price a
formula by averaging its truth value over the finitely many undisclosed atoms
appearing in that formula. This is a total computable rational market with an
explicit finite algorithm. It is not claimed to be efficient on arbitrary
input formulas, and it is not a finite-support belief state.

Every day is exactly coherent with `D_n`. Every fixed formula eventually has
all of its atoms disclosed, and thereafter has its correct Boolean value in
the all-true-atom model of `Gamma`. Nevertheless,

$$
P_n(A_n)=1/2\qquad(n\ge1),
$$

because `2^n>n`. This already fails the theorem-sequence conclusion of
Theorem 4.2.1. Here is also a direct exploitation proof, so the separation
does not rest only on importing that theorem.

Set `t_1=1` and `t_(j+1)=2^(t_j)`, giving purchase days
`1,2,4,16,65536,...`. Buy one share of `A_(t_j)` on day `t_j`, and make no
other trades. Each purchase costs `1/2`. By the next purchase day, the
previous atom has entered `D`; at most the latest purchased atom remains
undisclosed. At any day from `t_k` through `t_(k+1)-1`, cumulative assessed
wealth is

$$
W(H_n)=\frac{k-1}{2}+W(A_{t_k})-\frac12
\in\left\{\frac{k-2}{2},\frac{k}{2}\right\}.
$$

The possible wealth values are bounded below by `-1/2`. The all-true world
is always plausible and gives `k/2`, which is unbounded as purchase count
grows. The trader is admissible: its coefficients are constant continuous
features, and purchase-day membership can be decided in polynomial time in
unary `n`. Generate the tower only while its next value is at most `n`;
compare its exponent with `floor(log2(n))` before constructing a larger value.
Its output is either zero or the single trade `A_n-P_n(A_n)`.

Thus this market is exploitable under the original criterion. The example
separates mathematical duties; its deliberately slow use of an easy axiom
pattern is not a proposal for the strongest ordinary baseline. It gives no
finite challenge performance prediction.

### Witness 3: LI need not impose exact coherence on every finite day

Take a consistent `Gamma`-complete process with a sentence `theta` in `D_1`,
and any logical inductor over that process. Change only the first-day quote
of `theta` to `1/2`; keep every later pricing unchanged. The resulting market
is still a logical inductor by Theorem 4.6.1, but violates exact current
coherence on that first day: every world in `PC(D_1)` gives `theta` value one.

The theorem's finite-day invariance makes this a direct counterexample to
the alleged implication. Its theorem statement and explanation were checked;
the full Appendix G.7 proof was not independently rederived here. An interface
may still require exact correction at its next admitted update; that is an
additional finite requirement, not a consequence of the bare LI criterion.

There is also a representation reason to keep domains explicit. A globally
coherent pricing gives every syntactically distinct tautology price one.
With infinitely many such sentences it cannot have finite support. A finite
table with zero outside its domain is therefore different from an algorithm
that computes coherent prices on arbitrary requested formulas. Runtime of the
latter lookup must be accounted for; a day index is not a runtime guarantee.

## 4. Proofs, external executions and truth have different bridges

The current canonical contract correctly distinguishes truth, derivability
and receipt of a checked proof. The operational record should additionally
keep explicit execution/checking events typed:

| Record | What it establishes before any bridge | Required bridge for a stronger claim |
|---|---|---|
| `y_I(phi)` | Truth in the stipulated interpretation `I` | The interpretation and statement must be fixed |
| `Gamma_tau |- phi` | Derivability in the versioned theory/calculus | Calculus soundness and `I |= Gamma_tau` imply intended truth |
| A concrete checker accepts `(pi,phi,tau)` | An implementation returned acceptance on those bytes | Checker correctness implies the claimed derivation |
| A VM returns a bounded-program label or trace | An execution under specified VM/version/input/horizon conventions | Correct execution and encoding imply the corresponding operational truth; a checked formal certificate is needed to record it as a theorem by that route |
| A reasoner returns no answer within `B` | That procedure did not complete within its available budget | No truth or refutation conclusion follows without further evidence |

A correctly implemented complete simulation of the stipulated `b` steps can
decide the bounded claim even when the reasoner's available budget `B` is a
different quantity. A reasoner timeout before completing that test cannot be
substituted for the negative label. If an executor's output enters the state
as an observation rather than a formal proof, preserve that type and its
trust assumptions. A proved bridge for a concrete bounded-computation fragment
may turn an execution certificate into a formal proof; “we ran code” alone
does not supply the bridge for every implementation and formalization.

Consistency alone does not imply soundness for a chosen intended
interpretation. `Gamma`-completeness of disclosure does not make `Gamma` a
complete theory, decide independent sentences, or ensure intended arithmetic
truth. A finite checked log alone also does not establish completeness of
its infinite continuation. An adaptive paid discovery policy needs a separate
coverage argument before importing a property that requires `Gamma`-complete
disclosure. Its randomness and computability scope must be declared.

If the admitted hard record is inconsistent, an empty world set is a detected
inconsistency status, not a successful uncertainty estimate or action warrant.
If a premise is withdrawn or an interpretation changes, create a new scoped
active record. Such revision is not the same monotone deductive process.

## 5. Verification scope and resource record

Primary definitions and theorem statements were checked directly in the
131-page primary PDF, especially §§2–3.5, the §4 standing assumptions,
Theorems 4.1.1–2, 4.2.1 and 4.6.1. This is not an independent proof audit of
all imported LI properties. The projection identity and the first two
witnesses were reconstructed directly above; no empirical experiment or
novelty conclusion was inferred from them. No canonical file was changed.

Raw start observation: `2026-10-07T01:14:02.212858+00:00`,
`time.monotonic_ns() = 28811520077123`.
The completion observation below records elapsed span only, including any
tool, orchestration or compaction gaps. It is not an audited engaged-work
measurement and is **not added to the principal ledger**.

Raw completion observation: `2026-10-07T01:21:27.740099+00:00`,
`time.monotonic_ns() = 29257047240858`.
Observed elapsed span: `445.527163735` seconds. No principal credit.
