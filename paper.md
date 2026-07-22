# Value Logic: Scoped Reliance on Fallible Models Under Open-Ended Succession

Tristan Miano

## Abstract

Scientific models can be superseded while remaining useful on restricted
domains. We formalize this situation as a finite-stage, evidence-relative
license indexed by model, domain, task loss, fallback, tolerance, profile, and
provenance. An architecture-neutral factorization lets learned modules propose
reusable numerical statistics while exact checks preserve well-formedness,
atom states, masking, and fallback; finite ReLU networks provide one reference
realization. Retaining a reusable numerical statistic helped when the decision
threshold changed, but the conservative uncertainty-and-decoding pipeline often
converted informative predictions into abstentions. In the frozen synthetic
experiment, no-retraining tolerance transfer and marginal proposal coverage
were supported; boundary superiority and in-regime noninferiority were refuted
at their registered margins; usable coverage was poor. Formal results
characterize profile refinement, open-ended stability, update locality, robust
representation, and boundary obstructions. The project makes no claim of
architectural optimality, final truth, or true-utility recovery.

## 1. Introduction: Reliance Before Finality

Scientific succession creates a practical problem before it creates a final
verdict. A successor can restrict the range in which an older model is
dependable while leaving ordinary uses of that model intact. Meanwhile, an
agent with finite evidence, computation, and a finite library must decide what
to use now. The motivating question is therefore:

> Can a bounded agent represent present permission to rely on a fallible model,
> preserve the reasons and limits of that permission, and revise it as evidence
> and alternatives change?

Our answer is a finite-stage, profile-indexed license. It records whether an
evaluated use plan may presently be relied upon for a specified domain and
purpose, under named evidence, constraints, tolerance, fallback, comparison
set, and provenance. This is an operational judgment. The project remains
neutral about whether a current theory is finally true, and a license does not
turn task loss into a degree of metaphysical falsity. Truth, empirical
adequacy, usability, current selection, and archival retention remain distinct
questions.

The compressed notation $\Pi(M,D,\epsilon)$ is a useful way to expose the
design problem, but only $M$ and $D$ follow directly from local retention under
succession. A model may work on one domain and fail the demands of another.
The symbol $\epsilon$ acquires meaning only after a task loss, a domain-level
risk aggregation, and a reliance rule have been declared. It may come from an
external safety or precision requirement. It may instead be induced by the
agent's fallback: if the outside option has loss $J(B,D)$ and switching must
improve on it by $\Delta$, then the contextual ceiling is
$\epsilon_B(D)=J(B,D)-\Delta$. Beating that ceiling and satisfying an absolute
adequacy constraint are separate requirements; a poor fallback can be easy to
beat while the candidate remains unsuitable for use.

The entity called a “model” is also relative to the operation being assessed.
A single library entry may be an equation, a fitted predictor, or a finite
plan that composes models, translations, estimators, and a router. We retain
the internal structure when its errors and provenance matter, while permitting
the complete plan to be assessed as one use candidate. Such a plan can return
a payload, a quantitative grade or bound, and a certificate/provenance record.
The task's target loss, a learned estimator of that loss, and the optimizer's
training objective are typed separately. This permits finite, well-founded
recursive evaluation without postulating one universal unmodeled loss at the
end of every inquiry.

The paper makes four formal contributions:

1. **A finite-stage profile calculus.** A compact request separates the use
   plan, reliance context, epistemic state, and finite requirement profile.
   Well-formedness is checked before meaningful requirements receive supported,
   open, or refuted states. Their required meet yields Granted, Withheld, or
   Refused. We prove profile-refinement soundness and relative completeness on
   a finite independently realizable fragment within a fixed instantiation
   fiber.
2. **Constructive stability under open succession.** Continuation semantics
   distinguishes a present grant, eventual stabilization, permanent stability,
   scheme-relative certification, library completeness, and optional finality.
   Checked frozen dependencies and margin-separated sequential evidence give
   positive stability conditions. Finite non-domination remains relative to
   the searched library, so a later admissible candidate can change comparative
   status.
3. **Typed locality for revision.** Finite read footprints for the actual atom
   evaluators determine complete diagnostics, including negative collection
   reads. Disjoint writes preserve those diagnostics, and the canonical
   event-to-key-to-slot graph is change-complete under its stated realizability
   condition.
4. **An architecture-neutral representation with a ReLU reference.** The
   interface separates learned numerical proposals from exact evidence,
   well-formedness, decoding, masks, and fallback. We prove conservative
   recovery away from explicit error bands and give exact finite ReLU
   realizations for suitable finite continuous piecewise-linear statistics.
   Boundary collisions, scale, hard seams, and expandable libraries delimit
   the result.

ReLU compatibility was engineered at this typed boundary, delimited
mathematically, and tested in one frozen synthetic implementation. That test
gave an asymmetric result. Without retraining, the structured statistic arm
generalized strongly to changed tolerances (macro accuracy $.9436$ versus
$.7570$; paired difference $+.1866$, 95% interval $[.1860,.1873]$). Its
registered boundary-superiority proposition was refuted at its $+.05$ margin
(difference $-.2612$), and its in-regime-noninferiority proposition was refuted
at its $-.02$ margin (difference $-.1009$). The reverse comparisons were not
preregistered confirmatory claims. Marginal
target-in-proposal coverage was supported for the two registered groups
($.9098$ and $.9044$), while support/refutation miss rates were $.4611/.3248$
and target-weighted fallback mass was $.9962$. Thus:

> **Retaining a reusable numerical statistic helped when the decision threshold
> changed. But wrapping that statistic in a conservative uncertainty-and-decoding
> pipeline often turned informative predictions into abstentions.
> Representational information, calibrated caution, and operational usefulness
> are separate achievements.**

Conservative dead-band geometry is consistent with these observations. The
experiment did not identify how much of the effect came from the objective,
fit, calibration, interval construction, decoder, or their interaction. It
also was not an architecture comparison. ReLU is one analytically explicit
reference witness; the architecture-neutral interface admits other
realizations that preserve the same typed obligations.

An optional motivation concerns black-box policies. A value-like,
environment-relative surrogate is a promising high-level semantic view when
complete transparency is unavailable. A finite encoder-image existence result
and a conditional behavioral-reconstruction theorem make this bridge precise
at bounded scopes. The project does not investigate whether arbitrary policies
possess true utility functions, and it makes no claim that a surrogate recovers
true utility. Section 8 will keep representational existence, standard return
semantics, practical reconstruction, mechanism, and human interpretation as
separate questions.

Section 2 develops one succession decision and the origin of its tolerances.
Sections 3–5 introduce the finite calculus, continuation and update results,
and certificate-carrying composition. Sections 6–7 give the representation and
learning interfaces together with the frozen evidence. Section 8 presents the
optional policy/value motivation. Section 9 locates the claims among adjacent
literatures, and Sections 10–11 discuss the resulting boundaries and return to
the practical question.

## 2. One Succession Decision

### 2.1 From local usefulness to a reliance threshold

Let $M$ be a candidate use plan and $D$ the cases on which reliance is being
considered. A local loss $\ell_L(M,z)$ measures mismatch under a declared task
criterion $L$. A domain functional $\rho_D$ then gives

$$
R_{D,L}(M)=\rho_D\!\left(z\mapsto\ell_L(M,z)\right).
$$

Depending on the request, $\rho_D$ might be an expectation, a worst-case
operator, a tail functional, or an empirical estimate with its own uncertainty.
Only after these choices does the shorthand

$$
\Pi(M,D,\epsilon) \quad\text{suggest}\quad R_{D,L}(M)\leq\epsilon
$$

have an operational reading. The notation suppresses $L$, the aggregation,
the evidence supporting the bound, and the conditions under which the result
authorizes action. We therefore use it only as motivational compression; the
formal calculus will elaborate it into a complete request.

There are two common origins for $\epsilon$. An external rule may supply a
maximum acceptable error, failure probability, latency, or cost. A fallback
may instead supply a comparative origin. Let $J$ combine the task loss and
declared use costs, let $B$ be what the agent will do if no candidate is
selected, and let $\Delta\geq0$ be the improvement needed to justify switching.
Then

$$
s_B(M,D)=J(B,D)-J(M,D)-\Delta,
\qquad
\epsilon_B(D)=J(B,D)-\Delta.
$$

The candidate improves on the fallback when $s_B(M,D)\geq0$, equivalently
$J(M,D)\leq\epsilon_B(D)$. This comparison coexists with externally imposed
requirements. It does not certify the fallback as safe, and abstention inherits
the fallback's actual consequences.

### 2.2 A finite, synthetic succession

Consider four public names: an older local plan $M_{old}$, a broader successor
$M_{succ}$, a specialist $M_{new}$ that becomes available later, and fallback
$B$. The example is Newtonian-like only in its pattern of restricted retention.
Its numbers are synthetic and make no empirical claim about any physical
theory.

Take smaller-is-better task loss $J$. Since $J(B)=.35$ and switching must gain
$\Delta=.05$, the fallback-derived ceiling is

$$
\epsilon_B=.35-.05=.30.
$$

The request separately requires absolute adequacy $J(e)\leq.20$ and latency
$T(e)\leq50\text{ ms}$. At the initial stage, on an overlap,

$$
\begin{array}{c|cc}
&U_J&U_T\\ \hline
M_{old}&[.14,.18]&[43,47]\\
M_{succ}&[.11,.16]&[45,49]
\end{array}
$$

Both plans satisfy the displayed requirements and can be Granted. Simultaneous
licensing permits both uses; a router may still select one according to a
declared policy. On another region neither plan is licensed, so the explicit
fallback runs. A request in the wrong units is Undefined. A well-formed request
whose latency record is missing is Withheld.

At the next stage, the older loss certificate expires. Its relevant requirement
becomes open, and reliance is Withheld because the warrant has lapsed. Later,
accepted evidence $U_J(M_{old})=[.23,.25]$ supports the contrary side of the
$.20$ boundary, so that request is Refused. Lapse and rebuttal are different
revision paths.

Now tighten absolute adequacy from $.20$ to $.16$ while retaining the original
intervals. The older interval straddles the new boundary and remains open. The
successor is supported at inclusive equality. This reassessment requires no
learner retraining: the interval was reusable, and a changed decision followed
from a changed standard. At a later stage, $M_{new}$ fills the earlier gap.
Checked paired-difference certificates make it strictly better in loss and
latency than the displayed candidates on one exact finite overlap. It can
therefore become preferred there. The other models remain in the library and
may retain licenses on other scopes.

This example motivates the profile-indexed judgment selected for the paper.
The choice is an explicit interface design, rather than terminology forced by
the opening question. A profile says which adequacy, fallback, constraint,
trace, and finite-comparison requirements are mandatory and which are reported.
This lets current permission, comparative status, actual selection, and archive
retention change independently. It also keeps finite comparison honest: the
specialist dominates the exact evaluated set on the certified overlap; the
claim does not range over unexamined future candidates.

### 2.3 Granularity, recursion, and the representation question

For this request, each $M$ denotes an evaluated use plan. A plan can contain a
finite acyclic composition of predictors, converters, loss estimators, and
routers. Internally, each component keeps its identity and scope so that error
and provenance can be propagated. Externally, the complete plan can be assessed
as one candidate when the composition constructs a valid root grade and
certificate. This relative granularity blocks two shortcuts. Grants for
components do not automatically certify their composite, and a learned model
of the task loss is not the task criterion itself. Higher-order evaluation is
available through another typed request when its evidence graph is finite and
grounded.

The same distinctions create the neural representation problem. The scientific
object above is an overlapping licensed cover: several plans may be usable on
one case, there may be gaps, and selection occurs after licensing. A finite
ReLU network has its own activation complex, the polyhedral partition induced
by activation patterns. A router has a selection partition as well. These are
three mathematical objects, and no one-to-one correspondence among them is
assumed.

The hybrid interface gives learned modules a narrower job: propose named
statistics such as interval endpoints, risks, and margins. Exact external
machinery retains evidence identity, well-formedness, inclusive boundary rules,
profile aggregation, active masks, and fallback. For an accepted loss interval
$[l,u]$ at threshold $\epsilon$, the signed support margin is
$m_{support}=\epsilon-u$. Positive $\operatorname{ReLU}(m_{support})$ can expose
strict certificate-relative surplus for that named requirement. A zero
activation cannot finish the diagnosis: supported equality, an interval
crossing the boundary, and missing evidence can all yield zero. The exact state
and provenance resolve that collision. This is the typed seam at which the
paper's formal semantics meets its reference neural realization.

## 9. Related Work by Claim Boundary

### 9.1 Defeasible consequence, evidence, and succession

AGM belief revision formalizes contraction and revision of deductively closed
belief sets ([Alchourrón, Gärdenfors, and Makinson
1985](https://doi.org/10.2307/2274239)), while preferential and cumulative
logics characterize disciplined nonmonotonic consequence ([Kraus, Lehmann, and
Magidor 1990](https://doi.org/10.1016/0004-3702(90)90101-5)). Value logic shares
their concern with conclusions that survive some updates and fail after others.
Its output is instead a typed status for an empirical use request carrying
domain, loss, evidence, fallback, and provenance. Registry retention is also
separate from membership in a currently accepted belief set.

Input/output logic is the closest precedent for producing an output without
ordinary truth detachment ([Makinson and van der Torre
2000](https://doi.org/10.1023/A:1004748624537)). Labelled deduction and
justification logic motivate structured labels and explicit evidence terms
([Gabbay 1996](https://doi.org/10.1093/oso/9780198538332.001.0001); [Artemov
2008](https://doi.org/10.1017/S1755020308090060)). These precedents do not make
an empirical interval factive. Here a target-world conclusion needs an
explicit, mode-scoped evidence-to-world bridge; the finite-stage assessment is
usable operationally under that bridge.

Formal learning in the limit permits stabilization without a known final
arrival ([Gold 1967](https://doi.org/10.1016/S0019-9958(67)91165-5); [Kelly
1996](https://doi.org/10.1093/oso/9780195091953.001.0001)). This helps separate
eventual stabilization from a present certificate of permanence. Structural
accounts of scientific theories and intertheory relations likewise motivate
typed applications and bridges rather than a single undifferentiated
succession relation ([Sneed 1971](https://doi.org/10.1007/978-94-010-3066-3);
[Nickles 1973](https://doi.org/10.2307/2024906)). Our boundedness assumption is
operational: the current evidence, computation, registry, and search are
finite. The framework supplies no historical thesis that every scientific
succession has the same form.

### 9.2 Sequential uncertainty, abstention, and fallback

Classical sequential testing and confidence sequences supply stopping-time and
time-uniform uncertainty precedents ([Wald
1945](https://doi.org/10.1214/aoms/1177731118); [Darling and Robbins
1967](https://doi.org/10.1073/pnas.58.1.66)). Value logic imports no generic
validity from those names: each certificate still declares its population,
scope, procedure, and version. Selective classification gives the reject option
and the risk–coverage distinction ([Chow
1970](https://doi.org/10.1109/TIT.1970.1054406); [El-Yaniv and Wiener
2010](https://jmlr.org/papers/v11/el-yaniv10a.html)). Conformal prediction gives
finite-sample marginal coverage under exchangeability ([Shafer and Vovk
2008](https://www.jmlr.org/papers/v9/shafer08a.html)).

These tools occupy certificate and decision roles inside the framework. A
marginal prediction-set guarantee is not automatically a guarantee that task
risk is below $\epsilon$, that every profile requirement passes, or that routed
deployment is safe. Likewise, rejection prevents use of an unlicensed expert
while transferring the case to a fallback whose frequency and severity must be
measured. The frozen experiment makes this separation concrete: marginal
proposal coverage coexisted with near-universal target-weighted fallback.

### 9.3 Programs, proofs, and certifying computation

Program logic, refinement and quantitative types, proof-carrying code, and
certifying algorithms already provide compositional assertions, precise input
types, consumer-checked proofs, resource grades, and output-plus-witness
designs ([Hoare 1969](https://doi.org/10.1145/363235.363259); [Freeman and
Pfenning 1991](https://www.cs.cmu.edu/~fp/papers/pldi91.pdf); [Atkey
2018](https://doi.org/10.1145/3209108.3209189); [Necula
1997](https://doi.org/10.1145/263699.263712); [McConnell et al.
2011](https://doi.org/10.1016/j.cosrev.2010.09.009)). The paper's finite-plan
result is an integration at a mixed formal/empirical boundary: a constructor
jointly transforms payload, quantitative grade, and certificate/provenance, and
a checked root record feeds a defeasible profile assessment. Structural
induction and proof erasure are established machinery. An empirical confidence
region becomes a usable certificate only under its named validation mode; it
does not become a deductive proof merely by traveling with a computation.

### 9.4 ReLU representation and expert routing

Mixture-of-experts systems learn gates and local specialization ([Jacobs et al.
1991](https://doi.org/10.1162/neco.1991.3.1.79); [Jordan and Jacobs
1994](https://doi.org/10.1162/neco.1994.6.2.181)). A learned gate can route every
case, choose one expert when several are adequate, or specialize for reasons
unrelated to the scientific domains. It therefore does not supply an epistemic
license by itself.

Finite feed-forward ReLU networks compute continuous piecewise-affine maps, and
finite CPWL functions admit exact ReLU realizations under the cited conventions
([Arora et al. 2018](https://openreview.net/forum?id=B1J_rgWRW); [He et al.
2020](https://doi.org/10.4208/jcm.1901-m2018-0160)). Those representation facts
are inputs to the reference construction. The paper's application is the typed
factorization among learned statistics, exact states, diagnostics, masks,
registry, and fallback, together with explicit seam and boundary conditions.
Exact representability supplies neither an SGD recovery theorem nor evidence
that activation cells align with scientific regimes. The frozen experiment
addresses one trained implementation and reports the transfer-versus-coverage
trade-off; it does not establish architectural optimality.

### 9.5 Policy, value, and identification

Standard policy evaluation defines $V^\pi$ and $Q^\pi$ only after an
environment, return convention, state, horizon or discount, and perspective
are fixed; greedy use is governed by policy-improvement results ([Sutton and
Barto 2018](https://www.incompleteideas.net/book/the-book-2nd.html)). Revealed
preference can rationalize finite choices under explicit consistency
conditions ([Afriat 1967](https://doi.org/10.2307/2525382)). Inverse
reinforcement learning and later identifiability analyses show why behavior
alone generally leaves reward or reward-equivalence ambiguity ([Ng and Russell
2000](https://ai.stanford.edu/~ang/papers/icml00-irl.pdf); [Skalse et al.
2023](https://proceedings.mlr.press/v202/skalse23a.html)).

The optional bridge has a narrower constructive target. A fixed injective
finite action code gives an exact policy/value-like encoder-image
correspondence, and accepted score-error and action-gap evidence can certify
behavioral reconstruction on a named distribution. Standard return semantics,
off-support generalization, identification, mechanistic alignment, and human
interpretation require additional assumptions and tests. The project remains
neutral about whether an arbitrary policy has a true utility function.
