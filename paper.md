# Value Logic: Scoped Reliance on Fallible Models Under Open-Ended Succession

Tristan Miano

## Abstract

Newton's laws are considered superseded—“falsified” by modern physics in an
unrestricted sense—yet remain taught and used. Their continued use exhibits
pragmatic value: on a restricted domain, a fallible model may provide adequate
predictions at lower computational or operational cost than invoking a
successor. We expect present physics, including the Standard Model, to be
superseded in turn, without knowing whether the chain ends. We formalize such
value as a finite-stage, evidence-relative license indexed by domain, task
loss, fallback, tolerance, profile, and provenance. An architecture-neutral
factorization lets learned modules propose reusable statistics while exact
checks preserve states and fallback; finite ReLU networks supply one reference
realization. In a frozen synthetic experiment, tolerance transfer and marginal
proposal coverage were supported, registered boundary superiority and
in-regime noninferiority were refuted at their margins, and usable coverage was
poor. Formal claims remain neutral about final truth, architectural
optimality, and true-utility recovery.

## 1. Introduction: Reliance Before Finality

What does it mean for a model to be superseded? Newton's laws are a familiar
case. Modern physics supersedes—and, under an unrestricted reading,
“falsifies”—them. Yet college students still learn those laws, and Newtonian
models remain useful in engineering and other applications. We also expect the
Standard Model and other current fundamental frameworks to be superseded in
turn. On the motivating philosophical reading, this means that we regard even
our best present models as “false” when they are read as unrestricted final
descriptions: we expect future theories to expose limits that we do not yet
know. We do not know when this will happen, or even whether the chain of
supersession ends.

The continued use of Newtonian models supplies the link from that fallibilist
motivation to value. A successor may be more general or more accurate while
also requiring different measurements, calculations, expertise, or operating
costs. On a restricted domain, the older model may already keep the relevant
error below tolerance and may be easier to compute, inspect, or deploy. The
successor can therefore improve our account of the world without dominating
every bounded use. In this paper, **pragmatic value** is this task-relative
comparison: how well reliance serves a stated purpose under a named loss,
domain, and cost, relative to a successor, fallback, or other available plan.
The calculus does not define truth in terms of utility. It asks which reliance
is warranted while final truth remains unsettled. A model's pragmatic value
can survive the loss of an unrestricted truth claim, which is why supersession
naturally leads to a logic of licensed use.

That expectation is the paper's philosophical motivation, rather than a
premise proved by its formal results. It creates a practical problem before a
final verdict is available. A successor can restrict the range in which an
older model is dependable while leaving ordinary uses of that model intact.
Meanwhile, an agent with finite evidence, computation, and a finite library
must decide what to use now. The motivating question is therefore:

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

## 3. A Compact Finite-Stage License Calculus

### 3.1 Requests and their three operational carriers

The shorthand $\Pi(M,D,\epsilon)$ has now done its motivational work. Its
formal elaboration uses three principal carriers:

$$
E\quad\text{evaluated use plans},\qquad
Q\quad\text{reliance contexts},\qquad
S\quad\text{finite epistemic states}.
$$

An element $e\in E$ is a versioned executable plan: a predictor, equation set,
simulator, controller, or finite composition with a fixed interface. An
element $q\in Q$ packages the use question, including the typed domain $D_q$,
task, frame, target loss $L_q$, risk aggregation, acceptable region,
constraints, fallback $F_q$, required fallback advantage $\Delta_q$, and
certificate modes. An element $s\in S$ contains the agent's finite represented
library $K_s\subseteq_{\mathrm{fin}}E$, current records, evaluations, certificates,
searches, dependencies, and provenance. A transition $s\to s'$ appends a
declared event while preserving its history; a correction can invalidate an
old record's current force without erasing its occurrence.

Worlds $w\in W$ are semantic indices rather than operational inputs. They
interpret target quantities such as population risk that need not be
recoverable from the finite record. A request is

$$
\mathfrak r=(s,e,q,P)\in S\times E\times Q\times\mathsf{Profile},
$$

where $P$ is finite syntax selecting the requirements that matter. The
compressed expression $\Pi(M,D,\epsilon)$ is thus replaced by a request whose
loss, tolerance, fallback, evidence mode, and provenance are explicit.

A finite composed plan may expose an annotated result
$(\text{payload},\text{grade},\text{evidence})$. The payload performs the task;
the grade is a typed bound or resource quantity; and the evidence component
names the certificate, checker, scope, and provenance that warrant use of the
grade. This is only an interface here. Component successes do not by
themselves certify their composition; Section 5 will require a checked root
certificate.

The target criterion $L_q$, a learned estimator of $L_q$, and the optimizer's
training objective are distinct typed objects. A fallible estimator can itself
be represented by a plan and assessed through a higher-order request. The
ordinary core admits finite, well-founded towers of such requests. A genuine
self-referential cycle needs a separately specified fixed-point semantics.

Four judgments that can otherwise be called a “theorem” or “proof” remain
distinct:

| form | status |
|---|---|
| $[e,q]\varphi$ | an object-model output produced by plan $e$ for context $q$ |
| $\Gamma;s\vdash_{VL}J$ | an internal derivation in the frozen value logic from state-indexed premises |
| $\vdash_{meta}T(VL)$ | an external mathematical metatheorem about the calculus or implementation |
| $s\vdash_m\kappa:\mathsf{Claim}$ | a checker in certificate mode $m$ accepts evidence $\kappa$ for a typed claim |

An accepted empirical certificate belongs to the fourth row. Its consequences
for a target world depend on the declared soundness bridge; acceptance does
not silently turn it into a deductive proof of a world fact.

### 3.2 Profiles, typed atoms, and assessment

A profile is a finite collection of typed atom templates with slot identity.
The core examples are adequacy, improvement over the named fallback, hard
constraints, traceability, and two finite comparison requirements. A
relative-undefeated atom is supported when a valid declared search finds no
certified dominator in the exact evaluated set, and it is refuted when one is
found. A certified-undominated atom additionally requires every relevant
comparison in that set to be resolved as non-dominating or ineligible. Neither
ranges over unexamined future plans.
The basic reliance profile $P_{\mathrm{rely}}$ requires adequacy, fallback
improvement, hard constraints, and traceability. $P_{\mathrm{pref-rel}}$ adds
relative-undefeated status, while $P_{\mathrm{pref-cert}}$ adds the stronger
certified-undominated requirement.

Instantiating a template at the request base $(s,e,q)$ produces an address

$$
a=\mathsf{kind}(\text{parameters};\text{scope, criterion, mode}).
$$

The address retains enough type information to prevent a certificate for one
domain, loss, frame, candidate set, or checker mode from satisfying another.
Each slot is either **required** or **report-only**. A designated safety subset
of the required slots tells action consumers which unresolved or contrary
diagnostics must be exposed. Report atoms enrich comparison and explanation;
only required atoms determine authorization.

The predicate $WF(\mathfrak r)$ checks that all four request components denote, $e$ is
represented and executable on the requested cases, its output and frame match
$q$, the finite profile instantiates to typed addresses, comparison scopes are
exact, and action-authorizing profiles name a fallback. A wrong-unit latency
request in the running example fails $WF$ and is **Undefined**. Missing latency
evidence does not make the request ill typed; it leaves the latency atom open.

For every well-formed request, each required or report address has a total
finite-stage valuation

$$
\nu_s(e,q,a)\in K_3=\{-,?,+\},\qquad -<?<+,
$$

read as refuted, open, and supported. These are evidential states. The
calculus makes no three-valued claim about truth itself. For a current
nonempty certificate region $U_{\mathrm{cert}}$ and acceptable region $A$, the
common clause is

$$
U_{\mathrm{cert}}\subseteq A\Rightarrow +,\qquad
U_{\mathrm{cert}}\cap A=\varnothing\Rightarrow -,\qquad
\text{missing or boundary-crossing evidence}\Rightarrow ?.
$$

Fallback improvement uses its own comparison. With smaller-is-better loss,
candidate and fallback regions $U_{\mathrm{cert}}(e),U_{\mathrm{cert}}(F_q)$,
and required advantage $\Delta$, support requires
$\sup U_{\mathrm{cert}}(e)+\Delta\leq\inf U_{\mathrm{cert}}(F_q)$; separated
evidence on the contrary side refutes the atom, and overlap leaves it open.

At the initial state of the succession example, let $q_{.20}$ require
adequacy $J(e)\leq.20$, improvement by $.05$ over $B$ with $J(B)=.35$, latency
at most $50$ ms, and an accepted trace. The displayed loss and latency regions
for both $M_{old}$ and $M_{succ}$ support all four requirements, so both plans
can be licensed. Adequacy, fallback improvement, and comparative preference
remain separate: the first imposes an absolute $.20$ ceiling, the second
imposes the fallback-derived $.30$ ceiling, and a stronger profile may later
ask which plan is undefeated within an exact finite evaluated set.

Every valuation comes with exactly one indexed diagnostic:
$\mathsf{Support}$ with witnesses, $\mathsf{Open}$ with obstacles, or
$\mathsf{Refute}$ with counterwitnesses, always carrying provenance. Let
$\mathsf{Diag}(\mathfrak r)$ be the complete address-to-diagnostic map. For the nonempty
required address set, define

$$
\mu(\mathfrak r)=\bigwedge_{a\in\mathsf{Req}(P)}\nu_s(e,q,a).
$$

Assessment first checks well-formedness and then lifts this meet:

$$
\mathsf{Assess}(\mathfrak r)=
\begin{cases}
\mathsf{Undefined},&\neg WF(\mathfrak r),\\
\mathsf{Refused},&WF(\mathfrak r)\ \text{and}\ \mu(\mathfrak r)=-,\\
\mathsf{Withheld},&WF(\mathfrak r)\ \text{and}\ \mu(\mathfrak r)=?,\\
\mathsf{Granted},&WF(\mathfrak r)\ \text{and}\ \mu(\mathfrak r)=+.
\end{cases}
$$

Thus one refuted requirement defeats the request; with no refutation, one open
requirement withholds it; a grant requires support for every required atom.
The complete diagnostics preserve why these outcomes occurred.

Typed refinement records when support for one atom is sufficient for another
at the same scope, loss, frame, and certificate mode. Write $a\Rightarrow_A b$.
A smaller acceptable region refines a larger one, a larger required fallback
advantage refines a smaller one, and certified-undominated status refines
relative-undefeated status on the same finite comparison set. At the changed
adequacy threshold, for example,

$$
\mathsf{Adeq}(.16)\Rightarrow_A\mathsf{Adeq}(.20).
$$

The original interval for $M_{succ}$ supports the stricter atom at inclusive
equality, while the interval for $M_{old}$ crosses $.16$ and leaves that atom
open. A profile $P$ refines $Q$ when every required atom of $Q$ has a required
refining witness in $P$. At a well-formed request base
$\beta=(s,e,q)$, write this preorder as

$$
P\succeq_{prof}^{\beta}Q
\quad\Longleftrightarrow\quad
\forall b\in\mathsf{Req}_{\beta}(Q)\ \exists a\in\mathsf{Req}_{\beta}(P):
a\Rightarrow_A b.
$$

Section 4 will state the exact soundness and finite-fragment completeness
conditions; unmatched scopes or unrepresented interactions create no
refinement edge.

### 3.3 Licensed consequence, selection, and revision

Let $\Gamma\vdash_{(e,q)}\varphi$ be the internal evaluation relation supplied
by $e$ for $q$. When the request is Granted and $\varphi$ has the required type
and scope, the use rule produces a labelled output

$$
\Gamma\Rightarrow_{[s,e,q,P]}[e,q]\varphi.
$$

The label remains attached. Export to another domain, detachment as target
truth, or composition with another plan needs a separately validated bridge.
More precisely, a certificate mode $m$ declares admissible world/state pairs
$\mathcal C_m$. If its bridge establishes
$\mathsf{Support}_m(s,a)\Rightarrow\mathsf{Target}_w(a)$ for every
$\langle w,s\rangle\in\mathcal C_m$, then supported $m$-atoms receive exactly
that target-world conclusion. A statistical bridge carries only its stated
coverage or error guarantee.

Licensing precedes selection. For a case $x$, define the active set

$$
\mathsf{Act}(s,q,P,x)=\{e\in K_s:x\in D_q,\ \mathsf{Exec}_e(q,x),
\mathsf{Assess}(s,e,q,P)=\mathsf{Granted}\}.
$$

If it is empty, an action-authorizing selector may use only $F_q$ or a declared
information/abstention action. `NoLicensedModel` is a display derived from this
empty set, rather than an evidential atom. If the set is nonempty, a separate
$q$-indexed policy selects among it. A plan can consequently be licensed but
unselected, preferred on one finite overlap, or retained only in the library.

Under $s\to s'$, the old history remains addressable and every standing request
is recomputed from current diagnostics. Expiry of $M_{old}$'s loss certificate
therefore changes support to open and produces Withheld. The later region
$[.23,.25]$ lies beyond $.20$, producing a refuted adequacy atom and Refused.
Changing the tolerance from $.20$ to $.16$ changes $q$ and creates a linked new
request; it is a reassessment under a new standard. Adding and evaluating
$M_{new}$ can change a finite comparison atom and selection while leaving basic
licenses for old plans on other scopes intact.

### 3.4 Open-ended stages

To discuss succession, place the finite semantics in a continuation frame
$\mathcal F=(N,\to,n_0,\mathsf{state},\mathsf{world})$. Each node carries a
finite state and a semantic world index, and each compatible edge is a declared
history-preserving update. Fix the substantive query
$\chi=(e,q,P)$ and write

$$
A_\chi(n)=\mathsf{Assess}(\mathsf{state}(n),e,q,P).
$$

This fixed-query convention matters: replacing $e$, $q$, or $P$ asks a
different question. A **current grant** says only $A_\chi(n)=\mathsf{Granted}$.
For a path $(n_i)$, **eventual stability** and **permanent current stability**
are respectively

$$
\exists N,z\ \forall i\geq N:\ A_\chi(n_i)=z,
\qquad
\forall m\geq n:\ A_\chi(m)=A_\chi(n).
$$

The first definition does not imply that the agent recognizes the stabilizing
index. **Certified stability** adds a stage-local certificate whose named
verifier is sound for that continuation class. Finally, **semantic finality**
says that no proper continuation changes a declared projection of the whole
problem; it is external metalanguage and is stronger than stability of one
query.

These definitions permit constructive questions about which frozen
dependencies, evidence regimes, or live alternatives support each conclusion.
They do not place a `Final` predicate inside the base license language. The
calculus can therefore represent a useful present grant, later revision, and
even pathwise stabilization while leaving the philosophical endpoint of theory
succession open.

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
