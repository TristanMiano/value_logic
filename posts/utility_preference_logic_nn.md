# Utility- and Preference-Based Logics, and the “Logic” Implemented by Neural Networks

## Abstract

Utility- and preference-based logics replace (or refine) classical truth-conditions with semantic objects that encode *desirability*: real-valued utilities, multi-criteria vectors, or qualitative betterness relations. This shift forces three linked design choices: (i) *what semantic values are* (numbers, vectors, or ordered worlds), (ii) *what consequence means* (dominance, thresholds, comparative entailment, Pareto/lexicographic entailment), and (iii) *how connectives compose* (two-layer “classical + preference” systems, fully integrated many-valued semantics, or modal operators over ordered worlds). In parallel, modern neural networks already operate with real-valued scores, constraints encoded as losses, and optimization procedures that select parameters by minimizing a global objective. This suggests a precise sense in which neural networks implement a *utility-like semantics* and a *preference-like entailment*: learned models induce an ordering over hypotheses and outputs, and training drives the system toward states that better satisfy (weighted) constraints. Differentiable logic systems make this explicit by compiling logical structure into continuous operators and loss functions, providing a concrete bridge between preference semantics and gradient-based learning. [22][23][29][31]

---

## 1. From truth to value: what “utility-valued logic” is

### 1.1 Utility-valued vs preference-based semantics

A *utility-valued logic* is a formalism in which formulas are evaluated not merely as true/false, but as *values* that represent desirability—often real numbers, vectors of numbers, or elements of an ordered structure. A closely related family is *preference logics*, where formulas express and are evaluated by comparative relations such as “better than” or “at least as good as.” [1]

A useful minimal schema is:

- A base propositional language (with atoms and Boolean connectives).
- Additional preference/utility structure:
  - a numeric map $m(\varphi)$ into a value domain (e.g. $\mathbb{R}$, $\mathbb{R}^k$, or a poset), or
  - an ordering $\succeq$ over worlds, outcomes, or propositions. [1][3]

The conceptual point is not that truth disappears, but that “what follows from what” must be redefined so that consequence preserves *value* (utility, betterness, acceptability), not only truth. [1]

### 1.2 Ordinal and cardinal structure

Preference logics vary primarily by how much structure they assume about preference:

- **Ordinal**: only the ranking matters (e.g. $A \succ B$), with no meaning to differences in magnitude.
- **Cardinal**: utilities are meaningful up to positive affine transformation (as in vNM expected utility), supporting arithmetic combination and expectation. [2]

Decision-theoretic representation results clarify why this matters. Under suitable rationality axioms, preferences over options can be represented by an ordinal utility; and with stronger axioms over lotteries, one obtains cardinal utilities representable by expected value. This is the formal hinge that lets “preference” become “number” without changing choice behavior. [2]

---

## 2. A unified taxonomy: semantics → entailment → connectives

This section organizes three broad semantic designs (plus a fourth that is practically central) and then aligns them with entailment notions and connective behavior.

### 2.1 Semantic design A: scalar utility valuations for formulas

**Semantics.** Assign each formula $\varphi$ a value $m(\varphi)$ in a totally ordered (or partially ordered) domain. Van Dalen’s variants of Rescher-style semantics treat $m(\varphi)$ as a “measure of goodness” living in a poset, and interpret a primitive comparison $\varphi > \psi$ in terms of the order on $m(\varphi)$ and $m(\psi)$. [3]

A typical model-style picture is:
$M = \langle A, m, v \rangle$
where $v$ is a classical valuation for propositional structure and $m$ supplies values used by preference operators. [3]

**Natural entailments.**
- Comparative entailment: $\Gamma \models \varphi \succeq \psi$ iff all $\Gamma$-models satisfy $m(\varphi)\ge m(\psi)$ (or the relevant order convention). [1][3]
- Threshold entailment: $\Gamma \models m(\varphi)\ge c$ (satisficing / guarantees). [1]

**Connectives.**
Two standard styles appear:

1) **Two-layer:** Boolean connectives remain classical under $v$; preference operators use $m$. This recovers classical tautologies for $\land,\lor,\neg,\to$ while adding axioms governing $>$. [3]

2) **Integrated many-valued:** connectives operate directly on values, often via $\min/\max$ and a choice of negation and implication derived from a t-norm/residuum semantics. This makes “truth laws” like excluded middle nontrivial: with $\neg p = 1-p$ and $p \lor \neg p = \max(p,1-p)$, one gets $p\lor\neg p < 1$ whenever $p\ne 0,1$. [29][30]

---

### 2.2 Semantic design B: multi-dimensional (vector) utilities

**Semantics.** Values are vectors $m(\varphi)\in\mathbb{R}^k$, representing multiple objectives, stakeholders, or criteria. Comparison requires a rule: Pareto dominance, lexicographic priority, or scalarization. [1]

**Natural entailments.**
- **Pareto entailment:** $\Gamma \models \varphi \succ \psi$ if every admissible model makes $m(\varphi)$ at least as good componentwise and strictly better in at least one component. Pareto entailments are “safe” conclusions under unanimity-respecting aggregators. [1][17]
- **Lexicographic entailment:** if a priority order of criteria is assumed, comparisons become total (or closer to total), making entailment sharper but assumption-heavy. [1]

**Connectives.**
Vector semantics forces explicit choices about how disjunction and conjunction interact with control and aggregation. Many systems therefore keep Boolean connectives classical and define vector evaluation by aggregating over worlds/outcomes determined by the Boolean event. [1][5]

---

### 2.3 Semantic design C: ordered worlds (ordinal preference models)

**Semantics.** Models are possible-world structures $(W,\succeq,V)$ where formulas are true/false at worlds (as usual), but worlds are ranked by desirability. Preference operators or modalities quantify over “better” or “best” worlds. Modal preference and deontic logics fit here: “ought” can be interpreted as truth in the best accessible worlds. [1]

**Natural entailments.**
- Comparative entailment about propositions, often defined by lifting $\succeq$ from worlds to proposition extensions (sets of worlds) using quantifier patterns. [1]
- Deontic-style entailment ($O\varphi$ holds) as $\varphi$ holds in all best worlds, which is a special case of preference entailment via ideality order. [1]

**Connectives.**
The Boolean connectives stay classical *at each world*, but preference modalities do not distribute naively over $\land,\lor$. The logic’s interesting laws are interaction principles between preference operators and the Boolean core. [1][6]

---

### 2.4 Semantic design D: uncertainty + aggregation (expected value, worst-case, regret)

This is the planning-relevant bridge between preference logic and decision theory.

**Semantics.** Use:
$M=\langle W, P, U, V\rangle$
with utilities $U(w)\in\mathbb{R}$ and uncertainty $P$ over worlds. Then assign an “event utility” by an aggregation rule. The canonical choice is conditional expected utility:
$m(\varphi)=\mathbb{E}[U \mid \varphi]=\frac{\sum_{w\models\varphi}P(w)\,U(w)}{P(\varphi)}\quad\text{(if }P(\varphi)>0\text{)}.$
Other widely studied criteria replace expectation by worst-case (maximin), maximin expected utility over a set of priors, or minimax regret. [2][11][12][14]

**Natural entailments.**
- **EU dominance:** $\Gamma \models \mathbb{E}[U\mid \varphi] \ge \mathbb{E}[U\mid \psi]$ (comparative).
- **Maximin entailment:** prefer the option with better worst-case utility. [11]
- **Maxmin expected utility (multiple priors):**
$\varphi \succeq \psi$ iff $\min_{p\in\mathcal{P}} \mathbb{E_p}[U\mid\varphi] \ge \min_{p\in\mathcal{P}}$ $\mathbb{E_p}[U\mid\psi]$.
This is axiomatized as a rational choice rule under ambiguity aversion. [12]
- **Minimax regret:** define regret in state $s$ as the gap to the best available option’s utility in $s$, then choose the option minimizing maximum regret:
$\mathrm{Regret}(\pi,s)=U(\pi^{*}(s),s)-U(\pi,s),\ \pi=\arg\min_{\pi}\max_{s}\mathrm{Regret}(\pi,s).$
Regret-based criteria are central in preference elicitation and robust planning. [14][18]

**Connectives.**
Here connectives determine events (sets of worlds) and aggregation determines value; consequently, “utility of $\varphi\lor\psi$” is not truth-functional in $m(\varphi),m(\psi)$ alone—it depends on overlap and probabilities. [2]

---

### 2.5 “Which entailment goes with which semantics?”

A compact alignment (the “natural pairings”):

- **Scalar utilities** → comparative entailment, threshold entailment, dominance entailment among explicit alternatives. [3][2]
- **Vector utilities** → Pareto entailment, lexicographic entailment under priorities, admissibility under partial orders. [1][17]
- **Ordered worlds** → modal/deontic entailment via best worlds; comparative entailment via lifting. [1]
- **Uncertainty+aggregation** → EU entailment, maximin, maxmin EU, minimax regret; “optimality” becomes a theorem about an aggregation functional. [2][11][12][18]

---

### 2.6 Axiomatics for the basic preference connective $>$ and Rescher–Van Dalen semantics

This subsection makes explicit what is often left implicit in the “scalar utility / comparison” template: once you add a primitive comparative connective (read $\varphi>\psi$ as “$\varphi$ is (strictly) better than $\psi$”), you immediately face a choice between (i) *syntactic* principles for manipulating $>$-formulas and (ii) *semantic* constraints that explain which principles are valid. Classical preference logic is largely the story of lining those two up. [1]

#### 2.6.1 Classic $>$-principles (von Wright-style) as rewrite/normal-form constraints

A historically central approach treats $>$-statements as *atomic preference comparisons between situations*, and introduces principles that let you reduce complex preference claims to a standard form. Five representative principles (stated schematically) are: [1]

$V_1:\ (p>q)\rightarrow \neg(q>p)$ (asymmetry).

$V_2:\ (p>q)\land(q>r)\rightarrow(p>r)$ (transitivity).

$V_3:\ (p>q)\leftrightarrow((p\land\neg q)>(\neg p\land q))$ (expansion; “prefer $p$ to $q$” is analyzed via the $p\land\neg q$ vs $\neg p\land q$ contrast).

$V_4:\ (p\lor q)>(r\lor s)\leftrightarrow((p\land\neg r\land\neg s)>(\neg p\land\neg q\land r))\land((p\land\neg r\land\neg s)>(\neg p\land\neg q\land s))\land((q\land\neg r\land\neg s)>(\neg p\land\neg q\land r))\land((q\land\neg r\land\neg s)>(\neg p\land\neg q\land s))$ (disjunctive distribution; eliminates disjunctions inside preference comparisons by expanding into a conjunction of “casewise” comparisons).

$V_5:\ (p>q)\leftrightarrow(((p\land r)>(q\land r))\land((p\land\neg r)>(q\land\neg r)))$ (amplification; variables irrelevant to a preference comparison are held fixed by splitting on $r$). [1]

Two points matter for later “neural” analogies. First, these are not just algebraic curiosities: they are *normal-form* moves that make preference reasoning operational (often by reducing questions about complex $>$-formulas to collections of atomic comparisons). Second, they highlight a delicate issue: some powerful transformation principles (notably amplification) do not behave well with unrestricted substitution/replacement, so one must be careful about which inference rules are allowed if one wants a clean Hilbert calculus. [1]

#### 2.6.2 Rescher–Van Dalen measure semantics: models $\langle A,m,v\rangle$ and a completeness ladder

Rescher’s and Van Dalen’s semantic idea is strikingly close to the “utility-like” template in §2.1, but made completely explicit: interpret preference by comparing *measures of goodness assigned to propositions*. Van Dalen’s generalized models take the form $M=\langle A,m,v\rangle$, where: [1][3]

* $A$ is a partially ordered value domain (a poset; special cases include linear orders and $\mathbb{R}$),
* $m$ maps (classical) propositions to $A$ (the “goodness” measure),
* $v$ is an ordinary classical valuation for the Boolean backbone.

Preference is then evaluated by the order on $A$ (one common convention is “smaller is better”): $M\models \varphi>\psi$ iff $m(\varphi)<m(\psi)$. (If you prefer “larger is better,” simply reverse the order; the choice is not mathematically substantive, but it matters for reading formulas.) [1][3]

Van Dalen emphasizes that without further constraints, this semantics is *irrational* in a precise sense: logically equivalent formulas need not receive the same measure, so preference can discriminate between classically equivalent descriptions. To recover more familiar rationality constraints, he considers strengthening conditions on $m$ (or on $A$), notably: (i) equivalence-invariance (if $\vdash \varphi\leftrightarrow\psi$ then $m(\varphi)=m(\psi)$), (ii) linearity of the value order on $A$, and (iii) a real-valued “Rescher” specialization where $A=\mathbb{R}$ and $m(\neg\varphi)=-m(\varphi)$. [1][3]

Correspondingly, Van Dalen isolates a small family of Hilbert-style systems whose extra axioms track these semantic restrictions. Using $\equiv$ for indifference, defined by $\varphi\equiv\psi:=\neg(\varphi>\psi)\land\neg(\psi>\varphi)$, the core preference axioms are: [1][3]

$P_1:\ \neg(\varphi>\varphi)$.

$P_2:\ (\varphi>\psi)\land(\psi>\chi)\rightarrow(\varphi>\chi)$.

$P_3:\ (\varphi>\psi)\land(\psi\equiv\chi)\rightarrow(\varphi>\chi)$.

$P_4:\ (\varphi>\psi)\rightarrow(\neg\psi>\neg\varphi)$.

With classical propositional tautologies and modus ponens as background, Van Dalen’s named systems form a “completeness ladder” that matches the semantic constraints above: roughly, a minimal transitive/irreflexive base (PREFIR), then adding replacement to control substitutivity (PREF), then enforcing stronger equivalence sensitivity/linearity behavior (PREFL), and finally the Rescher-specialized behavior with $P_4$ (PREFR), with completeness results relating each proof system to its intended model class. [1][3]

This is the cleanest place where “preference logic” looks exactly like “utility semantics + comparison”: the connective $>$ is literally interpreted by an order on values, and proof theory is tuned to whatever invariances (logical equivalence, linear comparability, negation symmetry) you want the measure $m$ to respect. That structural picture is what later differentiable and neural instantiations inherit, replacing hand-specified $m$ with learned scoring functions and replacing purely symbolic consequence with optimization-driven selection among hypotheses. [1][3]


## 3. Meta-theory and feasibility: proof systems, completeness, and complexity

### 3.1 Mature proof systems: what is actually “well-developed”

Three families have relatively mature formal metatheory:

1) **Hilbert-style propositional preference calculi.** Van Dalen’s systems (variants of PREF) extend classical propositional logic with axioms constraining $>$ and prove soundness/completeness for corresponding semantic classes (weak posets; equivalence-respecting measures; linear orders; and real-valued-style constraints). [3]

2) **Modal (and dynamic) preference logics.** Preference orders over worlds admit modal axiomatizations, often inheriting canonical-model and correspondence machinery from modal logic. Dynamic preference upgrade logics provide a particularly crisp completeness story via reduction axioms that eliminate dynamic operators in favor of static ones. [6]

3) **Algorithmic preference formalisms (CP-nets and related ceteris paribus reasoning).** These often function as “proof procedures” operationally: dominance is answered by search in an improving-flip graph, and theoretical study focuses on complexity and structural tractability conditions. Their logical embeddings (e.g., ceteris paribus modal logics) then supply axiomatic metatheory where available. [8][5][7]

### 3.2 Soundness/completeness landscape (representative highlights)

- **Van Dalen completeness ladder.** A central result style is: *each axiom system corresponds exactly to a class of semantic models*. Weak systems match weak semantic assumptions; stronger axioms enforce stronger representability constraints (e.g. equivalence invariance; linearity; real-number-like behavior). [3][4]

- **Dynamic preference upgrade completeness.** When preference change is governed by a specified update rule, one can prove completeness by reducing preference-update modalities to a static base logic and then applying a standard completeness theorem. [6]

- **Ceteris paribus logics and finite model issues.** Modal logics designed to capture ceteris paribus reasoning can exhibit subtle model-theoretic behavior (notably, fragment-dependent phenomena that complicate “strong finitary” completeness narratives). [5]

### 3.3 Complexity: where the difficulty lives

Complexity varies dramatically with representation and query type:

- **Basic propositional preference logics** (with limited nesting and finite-model properties) are decidable and often live in NP / coNP-like territory for satisfiability/validity-style tasks, depending on the fragment. [3]

- **Modal preference logics** typically inherit PSPACE-completeness of modal satisfiability; dynamic extensions can rise to EXPTIME (mirroring dynamic logic / PDL-style complexity) for sufficiently expressive update operators. [6]

- **CP-nets dominance and consistency** are PSPACE-complete in general; tractable cases appear under acyclicity or bounded structural restrictions. [7][8]

These results strongly shape “what is usable”: planning systems rarely attempt general-purpose theorem proving in rich preference logics; instead, they compile to optimization, SAT/SMT, or specialized search procedures. [7][18]

---

## 4. Planning as the forcing function: why consequence must become preference-preserving

Planning highlights a mismatch: classical entailment is about *guaranteed truth*, while planning is about *choosing among achievable alternatives* based on soft goals, trade-offs, and uncertainty.

A standard framing distinguishes:

- **Classical planning with soft goals:** hard goals must be achieved; solutions are then compared by soft-goal satisfaction. [19]
- **Decision-theoretic planning (MDP-like):** actions induce probabilistic transitions and rewards; optimality is maximizing expected cumulative reward. [2][19]
- **Multi-objective planning:** plans map to vectors; one returns a Pareto front rather than a single optimum absent scalarization. [1]
- **Preference uncertainty:** the agent may not know the utility function precisely and must act robustly or elicit preferences. [18][12]

This is exactly where entailment notions like threshold, dominance, Pareto, maximin, and regret become “logical consequence” analogues: they specify what can be concluded about the relative desirability of plans under the premises. [1][2][18]

---

## 5. A micro-example where different logics provably disagree

Consider an agent choosing between two plans for a walk:

- $\pi_U$: take an umbrella.
- $\pi_{NU}$: do not take an umbrella.

World states: $R$ (rain) and $\neg R$ (no rain).

Outcome features:
- $Dry$ vs $Wet$.
- $Burden$ vs $NoBurden$.

### 5.1 Pure qualitative preference (incomparability)

Suppose the preference base includes:
$Dry \succ Wet,\qquad NoBurden \succ Burden.$
Then:
- Under $R$: $\pi_U \to (Dry \wedge Burden)$, $\pi_{NU}\to (Wet \wedge NoBurden)$, so $\pi_U$ is better (because $Dry\succ Wet$).  
- Under $\neg R$: $\pi_U \to (Dry \wedge Burden)$, $\pi_{NU}\to (Dry \wedge NoBurden)$, so $\pi_{NU}$ is better (because $NoBurden\succ Burden$).  

No dominance conclusion follows without an aggregation rule: the plans are incomparable given only ordinal ceteris paribus preferences. This is the typical “partial order” behavior of qualitative preference formalisms. [1][8]

### 5.2 Add a qualitative decision criterion: maximin vs maximax

Under **maximin**, compare worst-case outcomes:

- Worst($\pi_U$) = $Dry\wedge Burden$.
- Worst($\pi_{NU}$) = $Wet\wedge NoBurden$.

Since $Dry \succ Wet$, maximin entails $\pi_U \succ \pi_{NU}$. [11][20]

Under **maximax**, compare best-case outcomes:

- Best($\pi_U$) = $Dry\wedge Burden$.
- Best($\pi_{NU}$) = $Dry\wedge NoBurden$.

Then maximax entails $\pi_{NU} \succ \pi_U$. [20][9]

So the *same qualitative base* yields opposite conclusions depending on the adopted inference principle (decision criterion). [20][9]

### 5.3 Numeric expected utility: total ranking once probabilities/utilities are fixed

Let:
$U(Dry\wedge NoBurden)=100,\quad U(Dry\wedge Burden)=90,\quad U(Wet\wedge NoBurden)=-100,$
and $P(R)=0.2$. Then:
$EU(\pi_U)=90, \qquad EU(\pi_{NU})=0.2(-100)+0.8(100)=60,$
so $EU(\pi_U)>EU(\pi_{NU})$, hence $\pi_U\succ \pi_{NU}$. This is consequence-as-inequality in a cardinal semantics. [2]

### 5.4 Ordered-world (deontic) reading: “don’t get wet” as a priority

If a rule elevates “avoid wetness” lexicographically above inconvenience (an ideality ordering where any $Wet$-world is below any $Dry$-world), then $\pi_U$ is preferable because $\pi_{NU}$ admits an accessible $Wet$ outcome. This is preference entailment via best-world semantics. [1]

**Takeaway.** The disagreement is not noise; it is definitional. Each logic encodes a different notion of “what counts as following from the premises,” and planning forces those definitions into the open. [1][2][20]

---

## 6. Recommendation for uncertain-preference planning: a compact decision matrix

For planning under *uncertain or incompletely specified* preferences, three goals tend to matter simultaneously: (i) avoid catastrophic misalignment under plausible preference completions, (ii) remain explainable, and (iii) remain computationally implementable.

A strong practical recommendation is:

> Use a **two-layer design**: an **ordinal/constraint layer** to represent partial preference information, combined with a **robust decision criterion** (typically minimax regret or maxmin EU over a set of plausible utilities/priors), optionally transitioning to expected-utility optimization once elicitation sufficiently pins down the utility model. [18][12][2]

### 6.1 Why minimax regret is the sweet spot

- **Robustness:** minimax regret hedges against preference uncertainty without collapsing into extreme pessimism (as pure maximin can). [18][14]
- **Elicitation synergy:** minimax regret naturally identifies which preference queries reduce regret the most; this matches how interactive systems can ask “the next best question.” [18]
- **Logical fit:** it induces a strong consequence notion: “$\pi$ is (robustly) preferred” means its worst-case regret is no larger than alternatives’ across the admissible preference set. [18][12]

### 6.2 Implementation view

This recommendation is not a call for a bespoke theorem prover. It is a call for a semantics and entailment notion that compile to optimization: robust choice rules correspond to min–max problems and constraint-based search, which can be realized with contemporary optimization tooling and structured planning solvers. [17][18][19]

---

## 7. Do neural networks implement a logic?

The short answer is: neural networks implement *a family of value-based semantics* with an associated preference order, and differentiable logic systems show that this can be made literally logic-shaped. The longer answer is that there are (at least) two distinct “logic” senses in play:

1) **Inference-time semantics:** a network maps inputs to scores, probabilities, or graded satisfactions that behave like truth degrees or utilities.  
2) **Training-time entailment:** gradient-based learning selects parameters that better satisfy (weighted) constraints—an optimization-driven analogue of consequence.

Both are naturally interpreted through the utility/preference templates above, particularly the scalar and aggregation families. [22][23][29][31]

---

## 8. From propositions to scores: continuous semantics inside neural networks

### 8.1 Many-valued connectives as neural primitives

A broad thread in neurosymbolic work is that logical connectives can be interpreted as continuous operators over $[0,1]$ (or $\mathbb{R}$), with $\land,\lor,\to$ realized by t-norms and their residua, and quantifiers realized by $\min/\max$ or smooth approximations. This is precisely how “truth” becomes a graded score. [29][30][22]

A representative pattern (Łukasiewicz-style, for example) uses:
- conjunction: $p\otimes q = \max(0, p+q-1)$,
- disjunction: $p\oplus q = \min(1, p+q)$,
- implication: $p\Rightarrow q = \min(1, 1-p+q)$,
and builds losses from these semantics. [29][30]

This explains (in a controlled, formally studied way) why classical tautologies need not be “top-valued” in such semantics: excluded middle and non-contradiction become value inequalities, not universal equalities at 1 or 0. [29][30]

### 8.2 Explicit differentiable logics: LTN, LNN, semantic loss

Several systems make the “neural logic” claim concrete by construction:

- **Logic Tensor Networks (LTN)** implement “Real Logic,” a differentiable semantics where formulas evaluate to real degrees of satisfaction and learning minimizes loss terms derived from those logical constraints. [22]
- **Logical Neural Networks (LNN)** build a neural architecture that corresponds directly to weighted real-valued logical formulas, treating neurons as connectives and supporting forward/backward inference under graded truth. [23]
- **Semantic loss** defines a loss that is zero iff a propositional constraint is satisfied, derived from the constraint’s semantics; optimization then becomes “make the constraints true” in a graded sense. [31]

All three instantiate the same idea: a logic can be turned into a differentiable computation graph, and training is the process of satisfying formulas *as well as possible*, weighted by importance. This is utility-like semantics by any of the templates in §2: formulas map to scores, and “better models” are those with lower loss / higher satisfaction. [22][23][31]

### 8.3 Probabilistic and soft-constraint variants: PSL/HL-MRF and DeepProbLog

Another bridge goes through probabilistic soft logic and hinge-loss MRFs: weighted formulas compile into convex hinge-loss potentials, and inference becomes convex optimization over soft truth values. Here the “logic” is a system of soft constraints whose satisfaction is traded off by weights—again a direct instance of value-based semantics with optimization-based consequence. [30]

DeepProbLog integrates neural predicates with probabilistic logic programming: neural networks output probabilistic facts used in symbolic probabilistic inference, coupling graded truth with learning. [27]

### 8.4 From scores to open sets: the Heyting (intuitionistic/topological) semantics that drops out

A clean way to make “neural semantics” feel inevitable is to treat a proposition as a *continuous score* together with a *threshold truth region*. Let $Z=\mathbb{R}^d$ (or any topological space) and let a scalar statement be a continuous map $p:Z\to\mathbb{R}$. Associate to it the truth region $P={z\in Z: p(z)>0}$. Because $p$ is continuous and $(0,\infty)$ is open, $P$ is open.

Now order open sets by inclusion. The collection of opens $\mathcal{O}(Z)$ is a complete Heyting algebra, so it supports $\wedge,\vee,\top,\bot$ together with a Heyting implication and pseudo-complement negation. Concretely, the region-level operations are forced to be

* $P\wedge Q=P\cap Q$,
* $P\vee Q=P\cup Q$,
* $\neg P=\mathrm{int}(P^c)$,
* $P\to Q=\mathrm{int}(P^c\cup Q)$.

This immediately explains the “intuitionistic resonance” in continuous semantics: opens are not closed under complement, so excluded middle need not hold at the region level.

What matters for neural networks is that you can realize the set operations above *via score-level connectives that exactly track regions under the $>0$ cut*. If $p,q:Z\to\mathbb{R}$ are scores, define

* $(p\wedge q)(z)=\min(p(z),q(z))$,
* $(p\vee q)(z)=\max(p(z),q(z))$.

Then the induced regions satisfy ${p\wedge q>0}={p>0}\cap{q>0}$ and ${p\vee q>0}={p>0}\cup{q>0}$ by elementary properties of $\min/\max$. So “AND/OR” is not metaphorical here: min/max is literally the correct region semantics for a strict-threshold interpretation.

Even better: in ReLU networks these min/max operators are *exactly implementable* by affine maps plus ReLU. Writing $ReLU(x)=\max(0,x)$, we have the identities

* $\max(a,b)=b+ReLU(a-b)$,
* $\min(a,b)=a+b-\max(a,b)=a-ReLU(a-b)$.

So a ReLU net can compute lattice connectives on scores *exactly*, and therefore compute unions/intersections of the corresponding open truth regions exactly.

Negation in the Heyting/open-set semantics is pseudo-complement, $\neg P=\mathrm{int}(P^c)$. For a strict-threshold region $P={p>0}$, the complement is ${p\le 0}$, and typically $\mathrm{int}({p\le 0})={p<0}$ unless $p$ has a “flat zero plateau” on an open neighborhood. This makes the boundary behavior explicit: points with $p(z)=0$ are generally neither in $P$ nor in $\neg P$, and that is precisely where excluded middle fails in the induced region logic.

A similarly direct score surrogate for implication is

* $(p\Rightarrow q)(z)=\max(-p(z),q(z))$.

Then ${p\Rightarrow q>0}={p<0}\cup{q>0}$, which matches the Heyting implication $P\to Q=\mathrm{int}(P^c\cup Q)$ up to the same boundary subtlety (the difference between ${p<0}$ and $\mathrm{int}({p\le 0})$). In other words: once you adopt continuity + strict threshold truth + closure under min/max, the “open-set/Heyting” semantics is not an extra hypothesis—it is what your semantics collapses to at the region level.

### 8.5 Statements as vectors: closure principles that make “layer-by-layer logic” well-typed

The above picture becomes even cleaner if you treat “statement” as a *type* rather than a syntactic category.

A **scalar statement** is a map $p:Z\to\mathbb{R}$. A **vector statement** is a map $s:Z\to\mathbb{R}^n$. Vector statements aren’t a representational trick; they are what you get the moment you insist your system can carry many scalar statements together. Given scalar statements $p_1,\dots,p_n$, their bundled statement is the single object $s(z)=(p_1(z),\dots,p_n(z))\in\mathbb{R}^n$.

From here, three closure principles essentially force the standard neural-network pipeline:

1. **Closure under pairing/concatenation.** If $p,q:Z\to\mathbb{R}$ are statements, then $(p,q):Z\to\mathbb{R}^2$ given by $(p,q)(z)=(p(z),q(z))$ is also a statement. This is the minimal move that makes “reasoning about multiple propositions at once” possible without changing semantic universe.

2. **Closure under affine maps.** If $s:Z\to\mathbb{R}^n$ is a statement, then $a:Z\to\mathbb{R}^m$ defined by $a(z)=Ws(z)+b$ is a statement. This is the pre-activation map.

3. **Closure under pointwise nonlinearities.** If $a:Z\to\mathbb{R}^m$ is a statement and $\sigma:\mathbb{R}^m\to\mathbb{R}^m$ acts coordinatewise, then $s'(z)=\sigma(a(z))$ is a statement. This is the post-activation map.

Together these give the type-preservation claim you want in its sharpest form: pre-activations and post-activations live in the same semantic carrier, because both are simply vector-valued statements. A depth-$L$ network is then just a composition $Z\xrightarrow{s_0}\mathbb{R}^{n_0}\xrightarrow{f_1}\mathbb{R}^{n_1}\xrightarrow{f_2}\cdots\xrightarrow{f_L}\mathbb{R}^{n_L}$, where every intermediate object is still a “statement” (just at a different dimension).

Once you accept that, the earlier “logic inside the network” becomes a closure story rather than an analogy. Coordinates of $s(z)$ are scalar statements; pairing gives you $(p,q)$; and ReLU identities give you exact score-level connectives like $\min,\max$ (hence region-level $\cap,\cup$), plus the natural implication surrogate $\max(-p,q)$. That’s the sense in which “predicates on statements” and “statements themselves” share a single numeric universe: connectives are just functions $\mathbb{R}^k\to\mathbb{R}$ applied pointwise to bundled statements.

Finally, if the network’s purpose is choice or preference, there is a natural **preference interface**: a scalar head $U:Z\to\mathbb{R}$ that induces a preorder (and, in training, a scalar loss). Sigmoid and softmax are then simply alternative codomain constraints, $sigmoid\circ U:Z\to(0,1)$ and $softmax\circ U:Z\to\Delta^{k-1}$, which let the same internal statement calculus present as “degree of truth,” “probability-like score,” or “choice distribution,” depending on how the final layer is normalized. This is exactly the bridge that makes the later training-as-preference-entailment story feel structurally continuous with the earlier score/region semantics, and it aligns directly with the differentiable-logic frameworks already surveyed. [22][23][28][31]

### 8.6 Double negation in the open-set semantics: a ReLU witness, and why ReLU representations make it empirically salient

A particularly sharp way to see the intuitionistic/topological character of score-threshold semantics is to exhibit a concrete proposition $P$ where double negation strictly enlarges $P$, i.e. $\neg\neg P \not\subseteq P$.

Recall the open-set semantics from the previous section: for a continuous score $p:Z\to\mathbb{R}$ we take $P={z\in Z: p(z)>0}$, negation is $\neg P=\mathrm{int}(P^c)$, and double negation is $\neg\neg P=\mathrm{int}(\mathrm{cl}(P))$. Intuitively, $\neg\neg P$ “fills in” boundary points that cannot be separated from $P$ by any open neighborhood.

#### 8.6.1 A one-hidden-layer ReLU net with $\neg\neg P=\top$ but $P\ne\top$

Let inputs be $z=(x,y)\in\mathbb{R}^2$. Consider the ReLU network computing $p(x,y)=|x|$:

* hidden units $h_1=\mathrm{ReLU}(x)$ and $h_2=\mathrm{ReLU}(-x)$,
* output $p=h_1+h_2$.

Then $p(x,y)=|x|$, so the induced proposition is $P={(x,y): |x|>0}={(x,y): x\ne 0}$, i.e. the plane with the entire vertical line $x=0$ removed.

Compute negation:

* The complement is $P^c={(x,y):x=0}$.
* In $\mathbb{R}^2$, a line has empty interior, so $\neg P=\mathrm{int}(P^c)=\varnothing$.

Then double negation is maximal:

* $\neg\neg P=\neg(\varnothing)=\mathrm{int}(\mathbb{R}^2)=\mathbb{R}^2$.

So $\neg\neg P=\top$ but $P\ne\top$, and every point on the line $x=0$ satisfies $\neg\neg P$ while failing $P$. This is an explicit semantic witness that double-negation elimination fails: $\neg\neg P \not\Rightarrow P$.

#### 8.6.2 The “neither true nor false” region can be a whole manifold

On the entire line $x=0$ we have $p=|x|=0$, hence $(x,y)\notin P$ (since truth requires $p>0$). But also $(x,y)\notin\neg P$ because $\neg P=\varnothing$. So the full line $x=0$ is a nontrivial set of inputs where the proposition is neither true nor false under open-set negation, and it is exactly the locus where $\neg\neg P$ holds but $P$ does not.

This is a geometric form of the “boundary is undecided” phenomenon: with strict-threshold truth, boundaries belong to neither an open set nor the interior of its complement.

#### 8.6.3 Why ReLU makes this empirically visible: boundaries can carry probability mass in feature space

In raw Euclidean input space with a continuous sampling distribution, codimension-1 boundaries (lines, planes) have Lebesgue measure zero, so a random draw hits them with probability $0$. But neural networks do not only reason in the raw input space; they reason in learned feature spaces that include hard thresholding effects, and ReLU creates exact zeros on entire half-spaces.

A simple two-layer “feature space” version makes this explicit. Let raw inputs $(u,v)\in\mathbb{R}^2$ be drawn from any distribution symmetric in $u$ (e.g. standard normal). Define a ReLU feature map $x=\mathrm{ReLU}(u)$ and carry $y=v$, so the learned space is $Z=[0,\infty)\times\mathbb{R}$. Consider the score $p(x,y)=x$, with proposition $P={(x,y)\in Z: x>0}$.

Inside the subspace topology on $Z$, the set ${x=0}$ has empty interior (every neighborhood in $Z$ touches points with $x>0$), so $\neg P=\varnothing$ and $\neg\neg P=Z$ exactly as before. But now the “indeterminate line” ${x=0}$ is hit with non-negligible probability:

* $\Pr[x=0]=\Pr[u\le 0]=1/2$.

So half the samples land exactly on a set where $P$ fails and $\neg P$ fails, even though the same set would be measure-zero in a smooth ambient model. This is the core practical point: ReLU-induced representations can put atoms of probability on semantic boundaries, turning a topologically “thin” undecided set into an empirically frequent event.

(And the same mechanism scales: with two gated features $x=\mathrm{ReLU}(u)$ and $y=\mathrm{ReLU}(v)$ in $Z=[0,\infty)^2$, the conjunction score $p(x,y)=\min(x,y)$ yields $P={x>0\ \wedge\ y>0}$, while $P^c={x=0}\cup{y=0}$ has empty interior in $Z$, so again $\neg P=\varnothing$ and $\neg\neg P=Z$, and $\Pr[(x,y)\in P^c]=1-\Pr[u>0,v>0]=3/4$ for i.i.d. symmetric $u,v$.)

The upshot is that intuitionistic phenomena like $\neg\neg P\not\Rightarrow P$ are not just philosophical artifacts of open-set semantics: ReLU networks supply extremely small circuits whose strict-threshold propositions have large, structured “undecided” manifolds—and learned representations can concentrate probability mass on those manifolds.


---

## 9. Training as preference entailment: loss minimization induces an ordering

Let $\theta$ be network parameters and $f_\theta$ the model. Training data $\mathcal{D}$ and constraints $\mathcal{C}$ define an objective:
$\mathcal{L}(\theta)= \mathbb{E_(x,y)\sim\mathcal{D}}\big[\ell(f_\theta(x),y)\big] \;+\; \lambda \cdot \mathcal{L_\text{constraints}}(\theta),$
where $\mathcal{L_\text{constraints}}$ is built from differentiable logical semantics (e.g. semantic loss, t-norm formula losses, hinge-loss potentials). [31][29][30]

This induces a **preference relation over hypotheses**:
$f_{\theta_1} \succeq f_{\theta_2} \quad\text{iff}\quad \mathcal{L}(\theta_1)\le \mathcal{L}(\theta_2).$
In other words: *the model class is ordered by desirability*, and optimization is a procedure for moving upward in that order. This is exactly semantic design A (scalar valuation) applied to hypotheses rather than propositions, and it is the same structural move as decision-theoretic planning: choose the option that maximizes value (or minimizes cost). [2][28][31]

Moreover, when constraints are weighted, training implements a **trade-off logic**: satisfy higher-weight constraints preferentially, in the same sense that lexicographic or weighted-sum preference systems select among alternatives. [22][30]

---

## 10. Does the induced “logic” look like a preference logic?

Yes—if “preference logic” means “a system where consequence is defined by preservation or improvement of desirability.”

Three correspondences make the resemblance sharp:

### 10.1 Dominance/threshold entailment ↔ constraint satisfaction / feasibility regions

Many differentiable logic systems interpret a formula’s satisfaction degree as a score, and interpret constraints as defining a feasible region (or soft feasible region). A semantic loss is explicitly zero on satisfying assignments and positive otherwise, turning satisfiability into an optimization criterion. That is threshold entailment in the most literal sense: “good enough” is “loss ≤ ε,” and strict entailments become statements about the geometry of feasible sets. [31][30]

### 10.2 Comparative entailment ↔ score inequalities and margin constraints

Neural systems often learn inequalities like “class $y$ should score higher than class $y'$” or “this relation should hold more strongly than that one.” These are comparative preference statements. Logical neural networks and LTN-style semantics implement these as differentiable inequalities or ordering constraints over truth degrees. [23][22]

### 10.3 Aggregation under uncertainty ↔ probabilistic outputs and probabilistic logic coupling

When outputs are probabilistic (softmax, sigmoid) and combined with probabilistic logic layers, evaluation becomes an aggregation over uncertain states—mirroring the uncertainty+aggregation template. DeepProbLog makes this compositional: neural probabilities feed into symbolic probabilistic inference, and learning adjusts both neural and logical components. [27][2]

---

## 11. Intuitionistic resonances: why “no forced bivalence” shows up naturally

A recurrent motivation for intuitionistic and constructive logics is that truth need not be decided as 0/1 everywhere; instead, truth is tied to evidence or construction. Continuous semantics in neural systems similarly avoid forced bivalence: intermediate truth values are routine, and connectives are defined so that classical principles like excluded middle are not automatically top-valued. This is not “intuitionistic logic” in the strict proof-theoretic sense, but it is structurally adjacent: truth behaves like a graded resource, and implication is often implemented via residuated operations that resemble the role of implication in algebraic semantics. [29][22][23]

Differentiable logics that compile implication into differentiable operators and drive learning through loss provide a concrete mechanism by which “logical laws” become *optimization pressures* rather than absolute constraints. This is a distinctive shift from classical logic’s bivalent entailment, and it aligns more naturally with value- and preference-based semantics than with pure truth-preservation. [28][22][31]

---

## 12. What this suggests as a consolidated picture

A coherent synthesis is:

1) **Preference logics** provide semantic designs where formulas evaluate to desirability objects (numbers, vectors, or ordered-world modalities), and consequence is defined by preference preservation (dominance/threshold/comparative/Pareto). [1][3][2]

2) **Planning** forces these semantics to become operational: “entailment” must answer questions like “is plan $\pi$ undominated?” or “is $\pi$ optimal under criterion $C$?” rather than merely “is $\varphi$ true?” Robust criteria such as minimax regret supply principled entailment notions under preference uncertainty. [19][18][12]

3) **Neural networks**, as trained systems, already instantiate a value-based semantics:
   - inference yields graded outputs (scores, probabilities, satisfactions),
   - training defines a global objective,
   - optimization induces a preference order over hypotheses,
   - and differentiable logic frameworks make the connective structure explicit by compiling logic into loss. [22][23][30][31][28]

In this sense, the “logic implemented by neural networks” is most naturally classified as a *utility/preference logic with differentiable, often many-valued semantics*, where entailment is realized as improvement under an objective rather than derivability in a purely syntactic calculus.

---

## 13. Key assumptions (kept explicit) and what they buy you

1) **Cardinal vs ordinal.** Expectation and regret require interval/cardinal structure; pure comparative $>$ does not. Choosing the wrong structure makes certain inferences meaningless. [2][12][14]

2) **Uncertainty model.** A single $P$ yields EU; sets of priors yield robust criteria (maxmin EU, minimax regret). These induce different consequence relations. [2][12][18]

3) **Aggregation/decision criterion.** Maximin, maximax, minimax regret, and EU can disagree even on simple problems; adopting one is adopting a logic. [11][14][20]

4) **Constraint weights.** In differentiable logic, weights express priority/trade-offs; this is the numerical analogue of preference strength, and it determines which constraints are “entailed in the limit” of optimization. [22][30][31]

---

## Bibliography (consolidated)

1. Fenrong Liu and Leon van der Torre. “Preference Logic.” *Stanford Encyclopedia of Philosophy* (Fall 2025). https://plato.stanford.edu/entries/logic-preference/
2. Katie Steele and H. Orri Stefánsson. “Decision Theory.” *Stanford Encyclopedia of Philosophy* (Fall 2025). https://plato.stanford.edu/entries/decision-theory/
3. Dirk van Dalen. “Variants of Rescher’s Semantics for Preference Logic and Some Completeness Theorems.” *Studia Logica* 33(2), 163–181 (1974). https://doi.org/10.1007/BF02120492
4. Dennis J. Packard. “A preference logic minimally complete for expected utility maximization.” *Journal of Philosophical Logic* 4(2), 223–235 (1975).
5. Johan van Benthem, Patrick Girard, and Olivier Roy. “Everything Else Being Equal: A Modal Logic for Ceteris Paribus Preferences.” *Journal of Philosophical Logic* 38(1), 83–125 (2009). https://doi.org/10.1007/s10992-008-9085-3
6. Johan van Benthem and Fenrong Liu. “Dynamic Logic of Preference Upgrade.” *Journal of Applied Non-Classical Logics* 17(2), 157–182 (2007). https://doi.org/10.3166/jancl.17.157-182
7. Judy Goldsmith, Jérôme Lang, Mirosław Truszczyński, and Nic Wilson. “The Computational Complexity of Dominance and Consistency in CP-nets.” *Journal of Artificial Intelligence Research* 33, 403–432 (2008). https://doi.org/10.1613/JAIR.2627
8. Craig Boutilier, Ronen I. Brafman, Carmel Domshlak, Holger H. Hoos, and David Poole. “CP-Nets: A Tool for Representing and Reasoning with Conditional Ceteris Paribus Preference Statements.” *JAIR* 21, 135–191 (2004). https://doi.org/10.1613/jair.1234
9. Craig Boutilier. “Toward a Logic for Qualitative Decision Theory.” *KR-94*, 75–86 (1994). http://www.cs.toronto.edu/~cebly/Papers/_download_/kr94.pdf
10. Didier Dubois and Henri Prade. “Possibility Theory as a Basis for Qualitative Decision Theory.” *IJCAI-95*, 1924–1930 (1995). https://www.ijcai.org/Proceedings/95-2/Papers/115.pdf
11. Abraham Wald. “Statistical decision functions which minimize the maximum risk.” *Annals of Mathematics* 46(2), 265–280 (1945). https://www.jstor.org/stable/1969026
12. Itzhak Gilboa and David Schmeidler. “Maxmin Expected Utility with Non-Unique Prior.” *Journal of Mathematical Economics* 18(2), 141–153 (1989). https://doi.org/10.1016/0304-4068(89)90018-9
13. Teddy Seidenfeld, Mark J. Schervish, and Joseph B. Kadane. “A representation of partially ordered preferences.” *Annals of Statistics* 23(6), 2168–2217 (1995). https://projecteuclid.org/journals/annals-of-statistics/volume-23/issue-6/A-representation-of-partially-ordered-preferences/10.1214/aos/1038141103.full
14. Graham Loomes and Robert Sugden. “Regret theory: An alternative theory of rational choice under uncertainty.” *The Economic Journal* 92(368), 805–824 (1982). https://www.jstor.org/stable/2232669
15. Sven Ove Hansson. *Preference Change*. Springer (1995). https://link.springer.com/book/10.1007/978-94-015-8478-0
16. Jérôme Lang and Leendert van der Torre. “Reasoning with conditional preferences in the presence of soft constraints.” (2008). https://www.irit.fr/~Johan.Lang/papers/lncs5084.pdf
17. Aharon Ben-Tal, Laurent El Ghaoui, and Arkadi Nemirovski. *Robust Optimization*. Princeton University Press (2009). https://press.princeton.edu/books/hardcover/9780691143682/robust-optimization
18. Craig Boutilier, Radu Patrascu, Pascal Poupart, and Dale Schuurmans. “Constraint-based optimization and utility elicitation using the minimax decision criterion.” *Artificial Intelligence* 170(8–9), 686–713 (2006). https://doi.org/10.1016/j.artint.2006.02.003
19. Jorge A. Baier and Sheila A. McIlraith. “Planning with Preferences.” *AI Magazine* 29(4), 25–36 (2008).
20. Ronen I. Brafman and Moshe Tennenholtz. “On the Axiomatization of Qualitative Decision Criteria.” *AAAI’97*, 76–81 (1997).
21. Joseph Y. Halpern. “Defining Relative Likelihood in Partially-Ordered Preferential Structures.” *JAIR* 7, 1–24 (1997). https://doi.org/10.1613/jair.391
22. Samy Badreddine, Artur d’Avila Garcez, Luciano Serafini, and Michael Spranger. “Logic Tensor Networks.” arXiv:2012.13635 (2020). https://arxiv.org/abs/2012.13635
23. Ryan Riegel et al. “Logical Neural Networks.” arXiv:2006.13155 (2020). https://arxiv.org/abs/2006.13155
24. Tim Rocktäschel and Sebastian Riedel. “End-to-End Differentiable Proving.” arXiv:1705.11040 (2017). https://arxiv.org/abs/1705.11040
25. Richard Evans and Edward Grefenstette. “Learning Explanatory Rules from Noisy Data.” arXiv:1711.04574 (2018). https://arxiv.org/abs/1711.04574
26. William Yang, Wen-tau Yih, Roger Yang, et al. “Neural LP: Learning Logical Rules for Knowledge Base Reasoning.” arXiv:1702.08367 (2017). https://arxiv.org/abs/1702.08367
27. Robin Manhaeve et al. “DeepProbLog: Neural Probabilistic Logic Programming.” arXiv:1805.10872 (2018). https://arxiv.org/abs/1805.10872
28. Natalia Slusarz et al. “Logic of Differentiable Logics (LDL).” arXiv:2303.10650 (2023). https://arxiv.org/abs/2303.10650
29. Giuseppe Marra et al. “Learning and T-Norms Theory” (t-norm semantics to loss translation). arXiv:1907.11468 (2019). https://arxiv.org/abs/1907.11468
30. Stephen H. Bach et al. “Hinge-Loss Markov Random Fields and Probabilistic Soft Logic.” arXiv:1505.04406 (2015). https://arxiv.org/abs/1505.04406
31. Jingyi Xu et al. “A Semantic Loss Function for Deep Learning with Symbolic Knowledge.” arXiv:1711.11157 (2018). https://arxiv.org/abs/1711.11157
32. Logan Nye. “Categorical Construction of Logically Verifiable Neural Architectures.” arXiv:2508.11647 (2025). https://arxiv.org/abs/2508.11647
