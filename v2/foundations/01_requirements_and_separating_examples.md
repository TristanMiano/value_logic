# F01 — Requirements and Separating Examples

Research date: September 20, 2026 (America/Los_Angeles).
Source revision: `064320e9770cc796843da2de9335dce37cae2019`.
Status: worked requirements and examples; **not a selected calculus**.
Task completion and measured effort are recorded in the
[session record](../work_logs/F01_2026-09-20_S1.md).

## Durable findings

Eight small examples distinguish a value object from a particular evaluation,
and an available inference from a numerical operation that merely looks useful.
The central negative result is deliberately narrow: certain specified summaries
cannot answer certain specified composite queries. It is **not** an impossibility
of scalar value or an argument to encode every detail of a model.

The positive side matters equally. At a fixed task, a scalar comparison may be
exactly sufficient. Linear expectations of sums need no dependence information.
An expected minimum needs more than two means, but a suitable joint statistic
can suffice. Approximate pipeline outputs can be bounded using local errors and
sensitivity rather than evaluated anew. Complementary formal representations
can jointly answer questions neither answers alone. An exact bounded recoding
can preserve unbounded arithmetic if its operations are transported too.

These are conditional mathematical examples in a declared metatheory. No example
establishes a new soundness theorem for Value Logic, recovers metaphysical truth,
or selects its permanent carrier. Claim IDs and evidence status are in the
[claim ledger](../claim_ledger.md); notation is in [the glossary](../notation.md).
All numerical inputs below are constructed fixtures, not measurements of physics
or claims about the performance of deployed models.

## 1. Commitments, choices, and the meaning of a requirement

### 1.1 Fixed research commitments

The project proceeds without assuming direct access to final metaphysical truth.
It studies pragmatic reliance on revisable models relative to task performance,
tolerable error or reward, and resources. Its foundational direction is to
investigate value as the primary semantic object rather than require absolute
truth/falsehood as the operational primitive.

This does not entail that truth does not exist, that every model is false, that
all axiom systems are equally useful, or that one specific numerical algebra is
forced. We may prove conditional statements in ordinary mathematics while
explicitly declaring the assumptions of that metatheory.

### 1.2 Optional choices still open

Scalar, vector, function-valued, ordered, interval, and other representations
remain candidates. So do bounded and unbounded carriers, precise and imprecise
evaluation, different consequence relations, and different ways of representing
context. Probabilities in an example are stipulated task weights, not access to
a metaphysical distribution. A finite scenario index is a modeling device.

The phase-one license calculus and its evidence machinery are available results,
not mandatory primitives. Boolean recovery is a research target for a fragment,
not a reason to name arbitrary numerical operations conjunction or negation.
The following examples therefore specify questions and information access before
suggesting any representation that might answer them.

### 1.3 Three levels of obligation

**Honesty of an inference:** do not produce an exact answer, equivalence, or
ranking that the declared premises fail to determine.

**Desired expressive capability:** distinguish the paired cases in the admitted
fragment when the supplied inputs determine different answers. Always answering
“undetermined” is not a useful solution to a fully specified example.

**An explicit restriction:** a candidate may reject a query or support a narrower
fragment. Record the lost capability rather than call that rejection a failure
of every value-based calculus. No example makes its full query language a new
immutable philosophical commitment.

A separation has the form: two inputs have identical proposed summaries but
different required outputs. That refutes a decoder using only those summaries.
It does not refute a context-indexed scalar, an appropriate richer summary, an
interval answer, or a restricted query family. F02 will compare actual candidate
formulations; this note does not perform that selection.

## 2. E01 — A more accurate model need not be the better use

**Inputs and assumptions.** Use the declared reference function

$$
f(z)=z+z^3,
$$

and two available models: cheap $M_c(z)=z$, accurate $M_a(z)=z+z^3$.
The task evaluates mean absolute discrepancy on $D_a=\{-a,a\}$ with equal weights,
where $a>0$. The reference is part of this benchmark, not a claim about ultimate
physical reality. Use costs are $c_c=1$ and $c_a=8$ work units. A request supplies
an absolute error tolerance $\epsilon$, a work budget $b$, and an exchange rate
$\lambda$ in loss units per work unit. For this example only, comparison uses

$$
J_q(M)=R_a(M)+\lambda c_M,
\qquad R_a(M)\leq\epsilon,
\qquad c_M\leq b.
$$

The last two conditions are separate admissibility requirements; minimizing
$J_q$ does not erase either one.

**Question.** Which model should be retained and which selected as $a$, tolerance,
or resource conditions change?

**Derivation.** At either input, $|f(z)-M_c(z)|=|z|^3=a^3$. Thus

$$
R_a(M_c)=a^3,\qquad R_a(M_a)=0,
$$

and, when both are admissible,

$$
J_q(M_c)\leq J_q(M_a)
\quad\Longleftrightarrow\quad a^3\leq7\lambda.
$$

With $\lambda=1/1000$, $\epsilon=1/100$, and $b=8$:

| Scope | Cheap error | Cheap combined loss | Accurate combined loss | Result |
|---|---:|---:|---:|---|
| $a=1/10$ | $1/1000$ | $2/1000$ | $8/1000$ | both admissible; cheap is preferred |
| $a=1/2$ | $1/8$ | $126/1000$ | $8/1000$ | cheap violates tolerance; accurate is admissible |

At $a=1/10$, changing only $\lambda$ to $1/10000$ makes the combined losses
$11/10000$ and $8/10000$: accurate is preferred although cheap remains adequate.
At $a=1/2$ with budget $b=2$, neither candidate meets both requirements.
That is a gap in this candidate set, not evidence that an unspecified fallback
is acceptable.

There is an exact score-collision check as well. At $a=1/2$ and
$\lambda=1/56$, both combined losses equal $1/7$. Keeping
$\epsilon=1/100$ and $b=8$, however, only the accurate model meets the error
tolerance. Thus this particular combined-loss number, without additional
candidate information, cannot distinguish these two admissibility outcomes.

**Required distinction.** Accuracy, adequacy, resource feasibility, comparative
selection, and retaining an alternative are different questions. A value-based
inference should expose which task conditions justify changing a selection.
The example permits a scalar $J_q$ once the comparison contract is fixed; it
does not demand a vector primitive. Conversely, the scalar comparison alone
cannot answer admissibility unless its required side information is available.

**Not concluded.** The accurate model is not metaphysically true, the cheap model
is not universally preferable, and the chosen additive exchange rate is not a
universal account of resource value. Removing the declared reference or error
knowledge requires an evidence model, not reuse of these exact risk numbers.

## 3. E02 — Task changes reverse a ranking without inconsistency

**Inputs and assumptions.** A use produces two requested outputs, with reference
$(0,0)$. Models return $A=(0,4)$ and $B=(1,1)$. Both have equal use costs and
known absolute-error vectors $(0,4)$ and $(1,1)$. Task $q_\theta$, for
$0\leq\theta\leq1$, chooses their relative importance:

$$
R_\theta(M)=\theta e_1(M)+(1-\theta)e_2(M).
$$

Errors have been put in declared comparable loss units. Here $\theta$ expresses
task importance; it is not uncertainty about which output exists.

**Question.** Can one task-independent ordering of the two models reproduce all
these task-relative comparisons?

**Derivation.**

$$
R_\theta(A)=4(1-\theta),\qquad R_\theta(B)=1.
$$

Hence $A$ is better for $\theta>3/4$, $B$ for $\theta<3/4$, and they tie at
$\theta=3/4$. At $\theta=9/10$ the losses are $2/5$ and $1$; at
$\theta=1/10$ they are $18/5$ and $1$. A fixed scalar ordering that must answer
both strict comparisons cannot do so. A family of contextual scalar evaluations
can answer each question without contradiction.

There is also a useful uniform statement. For error vectors $u,v\in\mathbb R^2$,

$$
\theta u_1+(1-\theta)u_2
\leq\theta v_1+(1-\theta)v_2
\quad\text{for every }\theta\in[0,1]
$$

holds exactly when $u_1\leq v_1$ and $u_2\leq v_2$. The forward direction uses
$\theta=1$ and $\theta=0$; the reverse direction multiplies the two inequalities
by nonnegative weights and adds. Restricting the allowed tasks can change this
criterion. “All contexts” must therefore identify an actual family.

**Required distinction.** Retain the task or the information needed to answer
its queries. Distinguish “better here,” “better for every admitted task,” and
“neither uniformly dominates.” This is a capability requirement, not a decision
to make a Pareto order the fundamental value carrier.

**Not concluded.** Context-sensitive rankings are not irrational cycles, and the
example does not rule out scalar representations with contextual inputs. It
also does not justify adding errors measured in unrelated units without a
specified conversion.

## 4. E03 — Equal marginal evaluations can hide joint value

**Inputs and assumptions.** Two equally weighted scenarios give

$$
X=(3,-1),\qquad Y=(-1,3),\qquad Y'=(3,-1)=X.
$$

All payoffs use the same declared unit. Let $\mathbb E$ be the finite weighted
mean. The requested composite score is the mean of the pointwise minimum.
For this test, minimum is a stipulated bottleneck-score operation on jointly
indexed outcomes. It is **not** assumed to be logical conjunction.

**Question.** Can individual means determine the composite score? Do full
separate marginal distributions repair the problem?

**Calculation of the required starting witness.**

$$
\mathbb E X=\mathbb E Y=\mathbb E Y'=\frac{3-1}{2}=1.
$$

But

$$
\min(X,Y)=(-1,-1),\qquad
\min(X,Y')=(3,-1),
$$

so

$$
\mathbb E\min(X,Y)=-1,\qquad
\mathbb E\min(X,Y')=1.
$$

The maxima likewise have means $3$ and $1$. In both cases each input's marginal
law gives probability $1/2$ to $-1$ and to $3$. Consequently **even the pair of
complete marginal laws is insufficient** for this joint query. The missing
information is their alignment or dependence, not simply additional precision
in the two individual means.

**Exact separation argument.** Suppose $g$ computed every such composite mean
from the two component means. The first case would require $g(1,1)=-1$; the
second would require $g(1,1)=1$. This is impossible. Replacing “means” by
“marginal laws” leaves the identical-input/different-output argument intact.

**Positive controls.** First,

$$
\mathbb E(X+Y)=\mathbb E X+\mathbb E Y=2
$$

in both cases. This identity follows by adding finite sums, with no independence
assumption. It is false that all composition needs the entire joint law.

Second, the real identity

$$
\min(x,y)=\frac{x+y-|x-y|}{2}
$$

implies

$$
\mathbb E\min(X,Y)=
\frac{\mathbb E X+\mathbb E Y-\mathbb E|X-Y|}{2}.
$$

For the first pair, $\mathbb E|X-Y|=4$; for the aligned pair it is $0$.
The two means plus this one joint statistic answer this particular query.
This is information sufficiency, not a claim that obtaining the statistic is
cheaper than evaluating the target. It does not show that the same statistic
is closed under arbitrary nested composition or answers every other joint query.

**Required distinction.** An inference must retain, elicit, bound, or explicitly
lack the joint information its operation needs. A correct interval or an
underdetermined result is preferable to an unjustified exact answer; supplied
joint data should allow the two concrete cases to be distinguished.

**Not concluded.** No impossibility of real-valued semantic objects follows.
An unrestricted real code could encode structured data, and other scalar
summaries or restricted operations may suffice. The counterexample targets
these identified evaluations under this identified information restriction.
Nor does positive expected value of each input justify positive expected value
of their pointwise minimum: the first pair refutes that inference directly.

## 5. E04 — Sequential use needs sensitivity and interface scope

**Inputs and assumptions.** The ideal first stage is $f(z)=z$ and its
approximation is $\hat f(z)=z+1/100$. The ideal second stage is $g(u)=100u$
and its approximation is $\hat g(u)=100u+1/50$. Functions are defined on all
real inputs, so the perturbed input remains in their declared validity scope.
Use absolute discrepancy in the respective stage-output units.

**Question.** Do component error bounds $1/100$ and $1/50$ justify their unweighted
sum $3/100$ as an end-to-end bound?

**Derivation.**

$$
\hat g(\hat f(z))=100z+1+\frac1{50}
=100z+\frac{51}{50},
$$

while $g(f(z))=100z$. The actual output error is $51/50$, not at most $3/100$.
The first stage's error has been amplified by $100$.

There is a constructive replacement. Suppose
$|\hat f(z)-f(z)|\leq\delta$, the ideal downstream map $g$ is $K$-Lipschitz on
the relevant inputs, and $|\hat g(u)-g(u)|\leq\eta$ on the **perturbed** first
stage's reachable outputs. Then

$$
\begin{aligned}
|\hat g(\hat f(z))-g(f(z))|
&\leq |\hat g(\hat f(z))-g(\hat f(z))|
     +|g(\hat f(z))-g(f(z))|\\
&\leq\eta+K\delta.
\end{aligned}
$$

Here this is $1/50+100/100=51/50$, and equality is attained. The coefficient
converts first-stage output error into final-output error; ignoring its units
would already make the proposed unweighted sum suspect.

Two boundaries matter. Errors can cancel, so the bound is not generally an
identity. With $\hat g(u)=100u-1$ instead, the composed approximation is exactly
$100z$ although both stages differ from their reference functions. Also, a
threshold downstream map $g(u)=\mathbf1_{u\geq0}$ can turn inputs $-\delta/2$
and $\delta/2$ into outputs separated by $1$ for every $\delta>0$. Without a
regularity or margin assumption, small upstream error need not imply small
output error.

**Required distinction.** A useful inference can derive a composite guarantee
without an already supplied final score, but it needs task-relevant sensitivity,
typing, and reachable-scope assumptions. A claim about the second stage only at
unperturbed inputs cannot silently be applied at new inputs. For example, take
$f(z)=0$, $\hat f(z)=\delta>0$, $g(u)=0$, and $\hat g(u)=Mu/\delta$ for any
$M>0$. The second approximation is exact at the only unperturbed input, $0$,
but its composite error is $M$. With $K=0$, pretending its zero error at $0$
is a valid $\eta=0$ on the perturbed input would incorrectly predict zero
end-to-end error. This explicitly witnesses the missing-scope assumption.

**Not concluded.** All useful loss functions need not be Lipschitz. The example
identifies one valid rule under one set of premises, not a mandatory universal
calculus. Nor does an upper error bound determine actual composite error or
justify additive accounting for every resource. This is a simple specialization
of ideas already developed in the phase-one
[transport and routing note](../../formalism/08a_transport_routing.md), not a new
phase-two theorem about arbitrary plan graphs.

## 6. E05 — Incomplete evaluation is not inconsistency

**Inputs and assumptions.** The operational question is whether a use has
nonnegative value for every evaluation currently admitted by the stated
assumptions, with at least one admitted evaluation. Compare

$$
S_{\mathrm{precise}}=\{1\},\qquad
S_{\mathrm{uncertain}}=\{-1,3\}.
$$

No distribution over these sets is supplied. Both have midrange $1$; assigning
equal probabilities to the second set would be an additional assumption.

**Question.** Can a central value alone justify uniform nonnegativity? What
happens if two accepted sources cannot jointly be satisfied?

**Derivation.** Uniform nonnegativity holds for $S_{\mathrm{precise}}$ and fails
for $S_{\mathrm{uncertain}}$, which contains $-1$. The central value loses the
exact distinction needed for this robustness question. Conversely, on a
nonempty finite set the scalar minimum answers that particular sign question
exactly: $\min S\geq0$ iff every admitted value is nonnegative. The full set
is not necessary for every consumer. If genuine refinement
replaces a nonempty set $S$ by a nonempty subset $S'$, a universal bound holding
on $S$ still holds on $S'$. This follows directly from set inclusion. A revision
that retracts an assumption can instead enlarge or replace the set, so the
same persistence inference does not apply.

Now let two sources assert $S_A=\{1,2\}$ and $S_B=\{-2,-1\}$ for the **same
quantity in the same scope**. Their conjunction gives $S_A\cap S_B=\varnothing$.
Both

$$
\forall v\in\varnothing:\ v\geq0,
\qquad
\forall v\in\varnothing:\ v<0
$$

are vacuously true mathematical statements. Neither supplies the requested
nonempty justification for use. One must diagnose the incompatible premises,
revise acceptance, or make the intended inconsistency-tolerant interpretation
explicit. Quietly converting empty compatibility into a positive certificate
answers a different question.

Taking the union or its convex hull is a possible reinterpretation, not the
same conjunction of accepted claims. In particular, an ordinary uncertain
model with hull $[-2,2]$ and two mutually incompatible sources with that same
hull may need different diagnostics even when their conservative numerical
bounds happen to agree.

**Required distinction.** Preserve what the requested conclusion depends on:
a point evaluation, a nonempty range of permitted evaluations, or conflicting
premises. The consumer may need provenance or a conflict indication in addition
to a bound. Three-valued logic, intervals, and source sets are possible
implementations; this example does not make any one of them compulsory.

**Not concluded.** An uncertain case is not necessarily unfavorable; an empty
compatible set is not a highly favorable case; and mathematical vacuity has
not been refuted. This is a separation between a formally universal assertion
and the operational requirement that it have a nonempty admissible basis.

## 7. E06 — Toy axiom systems have different useful interfaces

**Inputs and assumptions.** Consider two toy equational presentations with
numerals built from $0,1,+$. Their intended finite structures are addition
modulo $2$ and modulo $3$. Call them $T_2$ and $T_3$. Specify the addition tables,
identity, and distinct named elements; in $T_3$, $2$ abbreviates $1+1$.
Closed numeral terms can be reduced using the declared table.

| Structure | Nontrivial addition-table entries | Example internal equation |
|---|---|---|
| $T_2$ | $1+1=0$ | $1+1=0$ |
| $T_3$ | $1+1=2$, $1+2=2+1=0$, $2+2=1$ | $(1+1)+1=0$ |

These are finite equational presentations with stipulated interpretations,
not competing unrestricted descriptions of ordinary integer addition.
Their symbols are interpreted in different declared structures. Combining both
example equations as premises about a single operation with $0+1=1$ and
$0\ne1$ would imply $1=0$; indexing the interpretation prevents that mistake.
No result about the independence or truth of substantial set-theoretic axioms
is being claimed by this finite example.

For an operational comparison, let $N$ be uniformly sampled from
$\{0,1,2,3,4,5\}$. Module $M_k$ returns only $N\bmod k$. An adapter receives this
returned residue, **not the original $N$** and not another information channel.
Two tasks request parity $P(N)=N\bmod2$ or the three-way residue
$Q(N)=N\bmod3$, with zero-one loss. Adapters may use arbitrary fixed functions
of the available residue; allowing randomized adapters will not improve the
bounds below.

**Question.** Is either formal representation uniformly more useful? What can
joint access provide?

**Derivation.** $M_2$ answers $P$ exactly, while $M_3$ answers $Q$ exactly. For
parity from $M_3$, each observed residue corresponds to the pair $r,r+3$, which
contains one even and one odd number. Any adapter is correct with conditional
probability at most $1/2$. For $Q$ from $M_2$, each parity fiber contains all
three residues equally often. Any adapter is correct with conditional
probability at most $1/3$. Randomization produces a weighted average of these
same success probabilities, not an improvement. Thus the best achievable losses
with the specified interfaces are

$$
\begin{array}{c|cc}
 & P & Q\\
M_2 & 0 & 2/3\\
M_3 & 1/2 & 0
\end{array}
$$

for these two tasks. Neither uniformly dominates the other.

Joint output $(N\bmod2,N\bmod3)$ distinguishes all six inputs:

```text
N       0      1      2      3      4      5
pair   (0,0)  (1,1)  (0,2)  (1,0)  (0,1)  (1,2)
```

Indeed, equal pairs would make the difference of two inputs divisible by both
$2$ and $3$, hence by $6$; within the stated range the difference must be zero.
A table lookup therefore recovers $N$ and answers both tasks exactly.

**Required distinction.** Keep internal derivability/interpretation separate
from usefulness for an external task, and preserve the interface under which
an information-loss claim was proved. Complementary representations can
compose without declaring one globally false or one universally superior.

**Not concluded.** If the adapter can read $N$, these impossibility bounds no
longer apply. A different input distribution or admissible adapter family can
also change them. The example neither ranks real foundational axiom systems
nor argues that logical consistency alone measures their pragmatic value.
It is a checkable test of scope, interpretation, and task-specific capability.

## 8. E07 — Unbounded values and bounded recodings are different questions

### 8.1 Unbounded magnitude and a failed operation-preservation claim

**Inputs and assumptions.** A task allows arbitrarily large finite benefits in
a declared numerical unit. Let $v_n=n$ for positive integers $n$; there is no
common finite upper bound. Consider the strictly increasing recoding

$$
h(x)=\frac{x}{1+|x|},\qquad h:\mathbb R\longrightarrow(-1,1).
$$

**Question.** Does monotone recoding by itself preserve the task's additive
combination and consequent rankings?

**Derivation.** Even $h(1)+h(1)=1$ differs from $h(2)=2/3$; the former is outside
the image's open upper endpoint. More operationally, compare two two-component
plans with additive benefits:

$$
A=(3,0),\qquad B=(1,1).
$$

Their original totals are $3>2$, but the sums of independently recoded components
are $3/4<1$. Naively retaining ordinary addition after recoding reverses the
comparison. Monotonicity preserves the ordering of an already computed total;
it does not automatically commute with computing that total.

This is **not** an impossibility of bounded representations. Since

$$
h^{-1}(y)=\frac{y}{1-|y|},
$$

the transported operation

$$
a\mathbin{\oplus_h}b=h\bigl(h^{-1}(a)+h^{-1}(b)\bigr)
$$

satisfies $h(x)\mathbin{\oplus_h}h(y)=h(x+y)$ exactly. For nonnegative $a,b<1$,
substitution simplifies it to

$$
a\mathbin{\oplus_h}b=\frac{a+b-2ab}{1-ab}.
$$

The denominator is positive on that domain. Thus exact recoding with translated
operations preserves these distinctions; naive recoding with unchanged
operations does not. No candidate has yet been selected on either basis.

Precision introduces a separate issue:

$$
h(n+1)-h(n)=\frac{1}{(n+1)(n+2)}\longrightarrow0.
$$

With a fixed absolute error bound $\eta>0$ on encoded outputs, intervals of
radius $\eta$ around sufficiently large adjacent encoded values overlap.
Their ordering is then not certified by those approximate codes alone, absent
additional information about the errors or original inputs. In fact, the same
midpoint code is within $\eta$ of both exact codes once their separation is
at most $2\eta$. This is a limit of that precision contract, not of exact real-number recoding.

### 8.2 A genuinely unbounded object with finite evaluation

Unbounded range across a family is not the same as an unbounded individual
payoff. To test the latter, take scenarios $k=1,2,\ldots$, declared weights
$p_k=2^{-k}$, and payoff $X(k)=k$. The weights sum to one and $X$ is unbounded.
Nevertheless its expected value is finite:

$$
\sum_{k=1}^{N}k2^{-k}=2-(N+2)2^{-N}\longrightarrow2.
$$

The finite identity follows by induction. At $N=1$ both sides are $1/2$.
Adding $(N+1)2^{-(N+1)}$ to the expression for $N$ gives
$2-(N+3)2^{-(N+1)}$, the expression for $N+1$. The remainder tends to zero: for $N\geq1$, the ratio of successive positive
remainders is $(N+3)/(2(N+2))\leq2/3$. The constant payoff $Y(k)=2$ has the same expectation but a different tail:

$$
\Pr[X\geq8]=\sum_{k=8}^{\infty}2^{-k}=\frac1{128},
\qquad \Pr[Y\geq8]=0.
$$

These are task-relative evaluations under a specified weighting law. They
show an unbounded payoff need not have an infinite expectation and that equal
expectations do not settle a tail-sensitive query. Its supremum is nevertheless
infinite; finiteness under one evaluation does not transfer to every evaluation.

**Required distinction.** Separate: (i) a globally bounded carrier, (ii) a carrier
whose individual objects are bounded but whose family has no common bound,
(iii) genuinely unbounded scenario-indexed objects, and (iv) a bounded code for
unbounded values. In particular, a space of individually bounded contracts can
already contain arbitrary finite constants; it should not be criticized as
though it necessarily imposed one global value ceiling.

**Not concluded.** Ordinary addition is not compulsory for every notion of
value. This is a conditional test when additivity is part of the operational
question. The example also does not authorize divergent expected values or
indeterminate expressions involving infinities; admitting them would require
additional choices. Nothing here proves that a bounded or unbounded primitive
is uniquely correct.

## 9. E08 — A best-outcome evaluation may require unavailable information

**Inputs and assumptions.** Reuse E03's two scenarios and actions
$X=(3,-1)$ and $Y=(-1,3)$. An action must be chosen **before** the scenario is
revealed. A randomized choice is independent of the unobserved scenario.
Alternatively, the agent may purchase a binary signal $S_{\mathrm{obs}}$ with symmetric
accuracy $p\in[1/2,1]$ at cost $\kappa\geq0$ payoff units, then choose an action.
Signal acquisition precedes the action, and its conditional law is stipulated.

**Question.** Does the computable value $\mathbb E\max(X,Y)=3$ describe an
attainable choice from the original information state?

**Derivation.** Without a signal, either fixed action has expected payoff $1$.
A random choice of $X$ with probability $r$ has payoff

$$
r\mathbb E X+(1-r)\mathbb E Y=1.
$$

Thus $3$ is not attainable by any such ex-ante choice. Perfect observation
would permit choosing the action paying $3$ in each scenario, attaining $3$.
These are different admissible plans, not different arithmetic conventions.

Under the noisy signal, following its indicated favorable action gives

$$
3p-(1-p)=4p-1,
$$

before signal cost. For symmetric noise and a uniform prior, the four
signal-dependent deterministic rules are: either constant action (value $1$),
following the signal (value $4p-1$), and reversing it (value $3-4p$). Since
$p\geq1/2$, following is optimal; random mixtures cannot improve the maximum.
With acquisition optional, attainable optimal value is therefore

$$
\max\{1,\ 4p-1-\kappa\}.
$$

The signal is at least as good as no acquisition exactly when
$\kappa\leq4p-2$. For $p=3/4$ and $\kappa=1/2$, the attainable net value is
$3/2$, between the no-signal value $1$ and the free perfect-information value $3$.

**Required distinction.** An algebraically defined payoff envelope can be an
upper bound or a counterfactual object without being an implementable choice.
Inference about what an agent can achieve must retain its information schedule,
admissible policies, and acquisition cost. Task-relative scalar policy values
can be sufficient after that information contract has been fixed.

**Not concluded.** Pointwise maximum is not inherently invalid; its operational
interpretation must be stated. The noisy-signal formula is not a theorem for
arbitrary priors, asymmetric noise, or costs. This example does not begin the
separate future inquiry-policy project; it prevents an oracle from being
silently introduced into the proposed calculus.

## 10. Three further checks on E03's positive summary result

These refinements ask whether apparently sufficient repairs generalize. They
remain small separating examples, not a commitment to a general probabilistic
semantics.

### 10.1 Missing information can still permit a sharp bound

If only $\mathbb E X=\mathbb E Y=1$ is supplied, finite means do not give a
finite universal lower bound on the bottleneck mean over all real-valued
finite-scenario payoffs. For $a\geq0$, take

$$
X_a=(1+2a,1-2a),\qquad Y_a=(1-2a,1+2a).
$$

Their means remain one while $\mathbb E\min(X_a,Y_a)=1-2a$ tends to negative
infinity. Each individual payoff is bounded; their allowed family has no common
bound. The always-valid upper bound is $\mathbb E\min(X,Y)\leq1$, from
$\min(X,Y)\leq X$. It is attained by $X=Y=1$.

Knowing E03's full two-point marginals changes the answer. Let
$t=\Pr[X=3,Y=3]$. The marginal probabilities force the joint table, with row
and column labels $3,-1$, to be

$$
\begin{pmatrix}t&1/2-t\\1/2-t&t\end{pmatrix},
\qquad 0\leq t\leq1/2.
$$

Consequently $\mathbb E\min(X,Y)=3t-(1-t)=4t-1$ lies in $[-1,1]$.
Every value in that interval is achieved by an allowed $t$. Thus $[-1,1]$ is a
sharp answer from these marginals, even though an exact point is not determined.
It would be unjustified to report that same lower bound from the means alone.
A candidate can gain useful, honest conclusions without inventing the missing
dependence or retaining a uniquely specified joint model.

### 10.2 Matching covariance still need not determine a bottleneck mean

Let both variables take values $-1,0,1$. Use two joint probability tables,
with rows indexing the first variable and columns the second in that order:

$$
P_+=\frac1{18}
\begin{pmatrix}3&0&3\\1&4&1\\2&2&2\end{pmatrix},
\qquad
P_-=\frac1{18}
\begin{pmatrix}1&4&1\\3&0&3\\2&2&2\end{pmatrix}.
$$

Every row and column sums to $1/3$, so both separate marginal laws are uniform.
Both means are zero and both variances are $2/3$. In either table the
cross-moment is zero: the four corner contributions $xyP(x,y)$ cancel.
Thus their covariance is also the same, zero.

The pointwise minimum table is

$$
\begin{pmatrix}-1&-1&-1\\-1&0&0\\-1&0&1\end{pmatrix}.
$$

Its expectation under $P_+$ is $(-6-1-2+2)/18=-7/18$; under $P_-$ it is
$(-6-3-2+2)/18=-1/2$. Marginal laws plus covariance are therefore still
insufficient for this nonlinear joint query. The specific statistic
$\mathbb E|X-Y|$ from E03 does distinguish these cases; covariance is not a
universal substitute for it.

### 10.3 Sufficient two-input information need not support nesting

Let three binary payoffs $(U,V,W)$ be uniform over either of these four-row
sets:

```text
even: 000, 011, 101, 110
odd:  001, 010, 100, 111
```

Each individual payoff is equally likely to be $0$ or $1$. Every pair has the
same uniform law on $00,01,10,11$ in both models, so even **all pairwise joint
laws** agree. But

$$
\mathbb E\min(U,V,W)=0\quad\text{in the even model},
\qquad
\mathbb E\min(U,V,W)=1/4\quad\text{in the odd model}.
$$

Only row $111$ makes the minimum one. Thus successfully evaluating a binary
operation does not establish that the retained information suffices after its
result is composed with a third object. A candidate must demonstrate its
closure claim, preserve additional joint information, or declare that nested
query unsupported. No general no-go result for structured scalar codes follows.

## 11. Requirements matrix and handoff

The requirements below are conditional on admitting the corresponding questions.
They are not additional unrevisable philosophical axioms.

| ID | Desired capability or distinction | Witness | Choice still open |
|---|---|---|---|
| R01 | distinguish accuracy, tolerance, resource feasibility, and selection | E01 | scalarized comparison with explicit constraints or another ordering |
| R02 | preserve task-relative versus uniform comparison | E02 | contextual scalars, finite task profiles, partial orders, other summaries |
| R03 | do not reconstruct a joint nonlinear value from insufficient summaries | E03, section 10 | retained dependence, query-specific statistics, bounds, or restriction |
| R04 | derive an informative composite consequence from scoped premises | E04 | the selected rule language, quantitative grades, exact or approximate inference |
| R05 | distinguish incomplete evaluation, valid refinement, and inconsistent premises | E05 | intervals, sets, provenance, other evidence semantics |
| R06 | keep axiom interpretation and adapter information access explicit | E06 | indexed theories, typed modules, transport maps, other contextual interfaces |
| R07 | assess unbounded values without confusing magnitude, integrability, and code range | E07 | numeric carrier, admissible functions, transported operations, precision contract |
| R08 | distinguish a formal payoff envelope from an attainable plan | E08 | policy scope, observation schedule, operational annotations |
| R09 | demonstrate positive sufficiency, not just information-loss examples | E01-E04, E06-E08 | a small useful fragment is acceptable; a universal unknown answer is not |

A representation should be evaluated relative to the exact consumer questions.
If two inputs are identified by a summary but some admitted question separates
them, that summary is insufficient for exact answers to that question. This is
the same elementary consumer-factorization issue already present in
[the first paper](../../paper.md), section 6.1; no novelty is claimed for it.
The present advance is to make the proposed phase's operational test cases and
its non-overclaim boundaries explicit.

For F02, compare at least three candidates on these fixed fixtures and access
conditions. Label each answer exact, bounded, underdetermined, or outside the
candidate's declared fragment. Explain both retained information and actual
inference operations; serializing an entire model into a real number is not by
itself an account of useful structure. Do not rank candidates until their
capabilities are worked out. No F02 carrier construction or Gate A decision has
been made here.

## 12. Evidence and scope

The arguments above are direct derivations and finite countermodels, written for
this task. Familiar constructions are not asserted to be novel. The external
foundations audit is F03 and has not been replaced by an unverified literature
summary. Tests in [the fixture module](../checks/f01_examples.py) check arithmetic
and finite enumerations; they do not prove the unrestricted claims of a future
calculus. Exact executable results and the scope of self-review are recorded in
[the session log](../work_logs/F01_2026-09-20_S1.md).
