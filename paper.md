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

## 4. Open Succession and Local Revision

### 4.1 Profile refinement at one finite stage

The first result says when one profile is genuinely stronger than another.
Fix a request base $\beta=(s,e,q)$ at which profiles $P,Q$ are well formed.
Let $P\models_{prof}^{[\beta]}Q$ mean that every model in the declared
base-local model class inside the fixed instantiation fiber that grants $P$
also grants $Q$. Recall that
$P\succeq_{prof}^{\beta}Q$ requires each atom of $Q$ to have a refining witness
among the required atoms of $P$.

**Theorem 1 (profile soundness and relative completeness).** Every sound typed
profile refinement preserves grants:

$$
P\succeq_{prof}^{\beta}Q
\quad\text{and}\quad
\mathsf{Assess}(s,e,q,P)=\mathsf{Granted}
\quad\Longrightarrow\quad
\mathsf{Assess}(s,e,q,Q)=\mathsf{Granted}.
$$

On a finite independently realizable atom fragment inside the instantiation
fiber $[\beta]_{P,Q}$, the converse characterization also holds:

$$
P\models_{prof}^{[\beta]}Q
\quad\Longleftrightarrow\quad
P\succeq_{prof}^{\beta}Q.
$$

The soundness proof projects each support witness along the typed atom rule and
then takes the finite meet. For relative completeness, if refinement fails at
a required atom $b$ of $Q$, take the downward closure of the required atoms of
$P$. Independent realizability supplies a finite state supporting exactly that
closure and leaving $b$ open; it grants $P$ and withholds $Q$. Appendix B gives
the construction.

For the running example, support at the stricter $.16$ adequacy boundary
transports to the otherwise identical $.20$ requirement. A grant under
$P_{\mathrm{pref-cert}}$ likewise transports to $P_{\mathrm{pref-rel}}$ and
then to $P_{\mathrm{rely}}$ on the same request base. The theorem does not
transport evidence across a changed domain, loss, frame, certificate mode, or
evaluated set.

Both restrictions in the second display do work. If the operational semantics
contains a genuine conjunctive law $a_1\wedge a_2\models b$ but the syntax has
only unary refinements, the profile requiring $a_1,a_2$ can semantically entail
$b$ without a single witness atom. If the state change also changes an
instantiated address or rule, the new base leaves $[\beta]_{P,Q}$. Schema-wide
completeness would need the fragment hypothesis and well-formedness transfer at
every base. Finally, a target-world twin can share the same supporting state
while differing in actual risk; Theorem 1 orders operational grants and does
not erase the mode-scoped world bridge.

### 4.2 What can stabilize under continuing inquiry?

A finite assessment can stabilize without announcing that its last change has
occurred. The obstruction is constructive rather than a general thesis about
unknowability.

**Theorem 2 (finite-prefix barrier).** Suppose two roots $n,n'$ expose
isomorphic finite states and the same current value $z$ for fixed
$\chi=(e,q,P)$. If the value is permanent from $n$ but some descendant of
$n'$ changes it, then no stage-local certificate scheme sound for both
continuations can certify permanent current stability at their common finite
state:

$$
n\sim_{fin}n',\quad A_\chi(n)=A_\chi(n')=z,\quad
\mathsf{StableNow}_\chi(n),\quad
\exists m'\geq n':A_\chi(m')\neq z
\quad\Longrightarrow\quad
\neg\mathsf{CertifiedStable}_\chi(n).
$$

A local verifier receives the same finite input at both roots. Acceptance at
one therefore implies acceptance at the other, where the live descendant
contradicts soundness. In the succession example, the current $M_{old}$ grant
can have one continuation containing only irrelevant records and another whose
next event expires its loss certificate. The shared prefix establishes the
current grant; it cannot distinguish those futures.

Positive stability results come from conditions that remove the live
alternative.

**Theorem 3 (two constructive stability regimes).** Let a deterministic atom
have a finite dependency projection and evaluator $v_a=f_a(\mathsf{dep}_a,
\mathsf{Rules}_a)$. If a checkable freeze certificate preserves those values,
denotations, and rule versions under every admitted event, then

$$
\forall m\geq n:\ v_a(m)=v_a(n).
$$

For a statistical adequacy atom with target risk $\theta$, threshold
$\epsilon$, and regions $C_i=[L_i,U_i]$, suppose coverage holds eventually,
$\operatorname{diam}(C_i)\to0$, and
$\gamma=|\theta-\epsilon|>0$. Then the atom eventually stabilizes as supported
when $\theta<\epsilon$ and refuted when $\theta>\epsilon$.

The deterministic clause is induction over declared events. The statistical
clause chooses one index after both eventual coverage and diameter below
$\gamma$ hold; inclusion then puts every later region strictly on the correct
side. A finite profile stabilizes after the maximum of its finitely many atom
indices and its well-formedness index. If simultaneous coverage has probability
at least $1-\alpha$, the statistical conclusion has that stated guarantee on
the declared sampling law.

These conditions separate two possible stories about $M_{succ}$. A locked
latency record and verifier can be permanently stable for a restricted event
class. Repeated loss estimates can stabilize under a valid shrinking-region
regime when true risk has margin from the threshold. At the changed $.16$
boundary, however, the current interval ending at equality supplies no
positive target margin. The theorem therefore gives no automatic stabilization
claim there. Likewise, a proof of $T(e)\leq50$ does not survive an admissible
correction to its units unless the correction path was excluded or frozen.

Statistical stopping also has a familiar finite-prefix limit. If opposite-side
laws are mutually absolutely continuous on every finite observation
$\sigma$-field, a regime declaration made at a finite stopping time with
positive probability under one law has positive probability under the other.
No procedure in that family combines uniform zero error with finite
positive-probability declarations on both sides. This is the classical
sequential-testing pattern behind the distinction between convergence and
certified arrival ([Wald 1945](https://doi.org/10.1214/aoms/1177731118);
[Kelly 1996](https://doi.org/10.1093/oso/9780195091953.001.0001)), rather than
a new impossibility principle.

Finite-library comparison has a directional boundary.

**Theorem 4 (open-library direction).** If a comparison atom for $e$ is
supported at $n$ and a compatible continuation can add and validly evaluate a
dominator $d$, then its present positive status is not permanently stable:

$$
\mathsf{Comp}_e(n)=+
\quad\text{and}\quad
\mathsf{AddDom}(e,q,n)
\quad\Longrightarrow\quad
\neg\mathsf{StableNow}_{\mathsf{Comp}_e}(n).
$$

The conclusion is polarity-specific. If an already accepted dominator remains
valid in every continuation, the refutation of $e$ can remain stable while the
library grows. In the example, adding $M_{new}$ defeats a required finite
non-domination atom for an older plan on the certified overlap, while
$P_{\mathrm{rely}}$ can remain Granted on another scope. The result therefore
supports revisable finite preference; it supplies no claim that every grant is
unstable or that every library must remain incomplete.

### 4.3 Typed locality and change-completeness

Current diagnostic provenance records why an atom has its present status. It
may omit an absent record whose future insertion would change that status.
Local revision therefore uses a derived finite read interface
$\mathsf{Read}_s(\mathfrak r,i)$ for profile slot $i$ and a finite write set
$\mathsf{Write}(u)$ for each event. Collection-index keys are read even when
their collections are empty. They make absence—no certificate, pair record,
or search trace—visible to a later insertion.

**Theorem 5 (complete-diagnostic locality and graph change-completeness).** For
fixed $(e,q,P)$ and evaluator versions, agreement on a slot's complete typed
read projection preserves its instantiated address, diagnostic payload,
provenance, and $K_3$ value:

$$
\mathsf{Env}(s;e,q,P)|_{\mathsf{Read}_s(\mathfrak r,i)}
=
\mathsf{Env}(s';e,q,P)|_{\mathsf{Read}_s(\mathfrak r,i)}
\quad\Longrightarrow\quad
\mathsf{Diag}_s(\mathfrak r,i)=\mathsf{Diag}_{s'}(\mathfrak r,i).
$$

Consequently,

$$
\mathsf{Write}(u)\cap\mathsf{Read}_s(\mathfrak r,i)=\varnothing
\quad\Longrightarrow\quad
\mathsf{Diag}_{s'}(\mathfrak r,i)=\mathsf{Diag}_s(\mathfrak r,i).
$$

The canonical graph with edges from events to written keys, keys to reading
slots, required slots to assessment, and assessment to grant is
change-complete: every actual change has a path from an event. Hence graph-path
absence is sufficient for robust invariance. The converse requires
path-realizability for the exact observable and update class; a conservative
graph may contain an inert path.

The proof is a finite case analysis over adequacy/constraint regions, fallback
improvement, trace, the two comparison modes, and $WF$. Deterministic
normalization ensures that equality preserves complete witness or obstacle
payloads, rather than only their polarity. Appendix B gives the footprint table
and proof.

This theorem distinguishes the example's update paths mechanically. An
archive-only event whose writes miss every relevant read key preserves the
complete $M_{old}$ diagnostic. Expiry writes its current-validity and region
indices, so preservation does not apply. Rebuttal writes a countercertificate
index, and adding plus evaluating $M_{new}$ writes the exact evaluated-set,
search, and pair indices used by comparison slots. Without an empty
`PairIndex` read, inserting the first dominator record would be a database-style
phantom: the diagnostic could change even though none of the previously extant
member keys changed. Predicate-locking and frame-rule ideas are established
analogies ([Eswaran et al. 1976](https://doi.org/10.1145/360363.360369);
[O'Hearn, Reynolds, and Yang 2001](https://doi.org/10.1007/3-540-44802-0_1)).
The theorem itself is the clause-by-clause locality result for this calculus,
without importing either database concurrency semantics or separation-logic
ownership.

## 5. Finite Composition, Routing, and Evidence

### 5.1 A checked composite is a new plan

Let a finite directed acyclic plan graph have root $o$. At node $v$, an
annotated executor returns

$$
\mathsf{Ann}_v(x)=\langle y_v,g_v,c_v\rangle,
$$

where $y_v$ is the ordinary payload, $g_v$ is a typed quantitative
grade—including an error bound and resource map—and $c_v$ is a certificate
term with checker identity and provenance. A constructor declares separate
payload, grade, and certificate transformers plus its interface, scope, frame,
and termination side conditions. The certificate transformer cannot declare
its own output valid; acceptance comes from the mode and checker named by the
request.

**Theorem 6 (annotated execution, erasure, and license lifting).** Suppose the
plan graph is finite and acyclic, edge types and frames match, payload and grade
transformers are total and deterministic, primitives have accepted typed
evidence, and every constructor has a locally sound certificate rule. Then the
root bundle is unique, its composite certificate checks, provenance is
preserved in topological order, and

$$
\mathsf{erase}(\mathsf{Ann}_o(x))=\mathsf{Run}_G(x).
$$

If the graph is reified as plan $e_G$, $WF(\mathfrak r)$ holds, the accepted
root grade supports the instantiated adequacy and constraint atoms, and every
other required atom is supported, then

$$
\mathsf{Assess}(s,e_G,q,P)=\mathsf{Granted}.
$$

The proof is topological induction: build each unique payload, transformed
grade, and checked certificate after its predecessors, then erase the
annotations. The second display is ordinary $WF+K_3$ assessment applied to the
checked root claim. Structural induction, proof erasure, program logic, and
consumer-checked proof-carrying code are established machinery; the scoped
integration here is that formal and empirical certificate modes can feed one
typed, defeasible license without identifying payload, bound, or evidence.

For the running example, a predictor followed by a unit conversion, loss
estimator, and router is one composed plan only after those interfaces and
grades are propagated. Two sequential components can each have checked error
$.06$ against a local $.10$ tolerance while their same-direction composite
error is $.12$. Both leaf requests may be Granted while the root adequacy atom
is Refused. Pairing certificate identifiers therefore cannot substitute for a
root propagation rule.

Grounding imposes a second condition. In a finite support derivation, every
indegree-zero support node must be a typed accepted base, and derived rules must
preserve their premises' provenance. For evaluator systems, assign a strict
finite rank so each node reads only fixed exogenous inputs and completed
lower-rank outputs.

**Theorem 7 (grounded and stratified assessment).** A finite acyclic support
derivation with typed bases grounds every supported required atom. A finite
ranked system of total deterministic evaluators has exactly one global
assignment of outputs, diagnostics, and assessments; if local rules preserve
grounding, the global assignment is grounded as well.

$$
u\to v\ \text{as an evidence dependency}
\quad\Longrightarrow\quad
\rho(u)<\rho(v)
\quad\Longrightarrow\quad
\text{unique assessment by induction on }\rho.
$$

This permits an independently evaluated, versioned value-logic implementation
to appear as an ordinary plan at a higher rank than its completed run records.
Its same-run grant cannot be its sole evidence. A one-node acyclic “support”
with no typed base is ungrounded; a closed pair in which each grant supports the
other is cyclic. Equations such as $g=g$ and $g=\neg g$ are respectively
nonunique and unsatisfiable in Boolean space, while changing to $K_3$ still
does not choose an operator or fixed point. A cyclic extension would have to
declare that machinery and prove its evidence bridge. Kripke–Kleene fixed-point
semantics supplies a neighboring established pattern
([Kripke 1975](https://doi.org/10.2307/2024634);
[Fitting 1985](https://doi.org/10.1016/S0743-1066(85)80005-4)), not a ready-made
semantics for these typed empirical licenses.

### 5.2 Routed use exposes fallback and selected-scope risk

A scientific licensed cover may overlap, but an executed router still induces
a measurable partition. Let $\mathcal G_j$ be the event on which expert $j$ is
selected and authorized, $\mathcal M$ the event on which an expert is selected
outside the declared authorized/reference set, and $\mathcal B$ the explicit
fallback event. These events partition the deployment population.

**Theorem 8 (routed-risk decomposition).** For nonnegative integrable routed
loss,

$$
R(h)=\sum_j\mu(\mathcal G_j)R_{\mathcal G_j}(\ell_j)
+\mu(\mathcal M)R_{\mathcal M}(\ell_h)
+\mu(\mathcal B)R_{\mathcal B}(\ell_F).
$$

If the three conditional terms are bounded by
$\epsilon_j,L_M,L_F$, respectively, then

$$
R(h)\leq
\sum_j\mu(\mathcal G_j)\epsilon_j
+L_M\mu(\mathcal M)+L_F\mu(\mathcal B).
$$

The proof splits the loss integral over the finite partition. It also shows
why a router is a new evaluated plan: its risk depends on selected-subset loss,
misrouting, fallback frequency, and fallback severity, rather than only on the
licenses of its experts.

In the succession example, $M_{old}$ and $M_{succ}$ may both be licensed on an
overlap, $M_{new}$ may later be selected on a certified subregion, and the gap
goes to $B$. A parent-domain mean does not automatically certify a selected
subdomain. With loss $1$ on a $10\%$ subset and $0$ elsewhere, parent risk is
$.1$ while the bad subset has risk $1$. A router that selects precisely that
subset exposes the hidden loss. Likewise, the core fallback rule blocks an
unlicensed expert but permits a fallback whose target loss is catastrophic.
Theorem 8 therefore requires fallback mass and severity beside coverage; target
safety of $B$ needs its own evidence.

### 5.3 Quantitative grades propagate along paths

For a finite plan DAG, let $\delta_v$ bound intrinsic error at node $v$ on the
full reachable perturbation tube, and let $L_{u,v}$ be a certified downstream
Lipschitz factor on edge $u\to v$. Let $W_{u,o}$ be the sum, over paths from
$u$ to root $o$, of the products of their edge factors.

**Theorem 9 (path-sensitivity certificate).** The root error satisfies

$$
e_o\leq\sum_{u\in V}W_{u,o}\delta_u.
$$

If the outer task loss is $K$-Lipschitz on the reached range, the corresponding
two-sided risk difference is at most
$K\sum_uW_{u,o}\delta_u$. Repeated substitution in a topological order proves
the bound; Theorem 6 can carry the same arithmetic as the root grade and
certificate.

This result identifies the assumption missing from naive component addition.
An upstream error $\delta$ followed by the map $y\mapsto Ky$ produces error
$K\delta$, and a downstream certificate checked only at the nominal input need
not hold at the perturbed input. For the composed succession plan, local bounds
must cover the reachable tube and must be weighted by the unit converter,
estimator, and router sensitivities. Resource grades remain separately typed:
energy may add, latency may follow a critical path, and peak memory depends on
schedule. These composition and routing results constrain later
representations without selecting a neural architecture; that question begins
in Section 6.

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

## Appendix A. Core Syntax and Elaboration Reference

This appendix collects the exact finite core used by the proofs. It is a
reference presentation of Section 3, rather than a second operational API.

### A.1 Carriers and dependent fields

The three carriers and semantic index have the following interfaces:

| object | dependent data used by the core |
|---|---|
| $e\in E$ | versioned plan identity; $\mathsf{In}_e(q)$, $\mathsf{Exec}_e(q,x)$, output type, and frame |
| $q\in Q$ | cases and domain; task and frame; target loss $L_q$ and risk aggregation; ordered risk space and acceptable region; fallback $F_q$ and advantage $\Delta_q$; constraints and certificate modes |
| $s\in S$ | finite represented library $K_s$; records, evaluated set, certificates, searches, dependencies, provenance, and current-validity state |
| $w\in W$ | target risk, target constraints, and optional target truth used only by a declared bridge or metalanguage |

Changing a plan version, preprocessing rule, solver, or deployment wrapper can
change $e$. Changing domain, task, loss, tolerance, fallback, frame, or
constraint changes $q$. Appending an observation, correction, certificate,
search, or model addition changes $s$. An edge $s\to s'$ preserves an
injective embedding of historical events while permitting their current
validity to change.

A profile is the finite tuple

$$
P=(I_P,\mathsf{kind}_P,\theta_P,\mathsf{role}_P,\mathsf{Safe}_P).
$$

$I_P$ supplies slot identity; $\mathsf{kind}_P$ names a typed template;
$\theta_P$ instantiates its parameters from $(s,e,q)$;
$\mathsf{role}_P$ is required or report-only; and $\mathsf{Safe}_P$ selects
required slots whose open or refuted diagnostics must be exposed. The frozen
atom kinds are `Adeq`, `Improve`, finite families of `Constraint`, `Trace`,
`RelUndom`, and `CertUndom`. An address contains its exact candidate, domain,
loss, frame, criterion, evaluated set, and certificate mode whenever those
fields are applicable.

### A.2 Well-formedness, diagnostics, and assessment

For $\mathfrak r=(s,e,q,P)$ and $\beta=(s,e,q)$,
$WF(\mathfrak r)$ requires: the four components
denote; $P$ is finite and has a required slot; $e\in K_s$; the requested plan
is executable; output and frame interfaces match; every slot instantiates to a
typed address; comparison addresses name an exact finite scope, set, and
criterion; action-authorizing requests have an explicit fallback; and all
units, constraints, and modes are meaningful. `WFDiag` records the first
canonical failed obligation. Missing evidence occurs after $WF$ and produces
an open diagnostic.

For every instantiated required or report address, deterministic normalization
of current records yields exactly one of

$$
\mathsf{Support}(a,\text{witnesses},\text{provenance}),\quad
\mathsf{Open}(a,\text{obstacles},\text{provenance}),\quad
\mathsf{Refute}(a,\text{counterwitnesses},\text{provenance}).
$$

Their constructors determine $\nu_s(e,q,a)=+,?,-$, respectively. The common
clauses are:

| atom | supported | refuted | open |
|---|---|---|---|
| `Adeq` or region constraint | current certified region is contained in the acceptable region | the two regions are disjoint | missing, conflicted, or boundary-crossing evidence |
| `Improve` | $\sup U_e+\Delta_q\leq\inf U_F$ | $\inf U_e+\Delta_q>\sup U_F$ | missing or overlapping comparison |
| `Trace` | named verifier accepts a dependency-complete trace | valid hard countertrace | missing, expired, conflicted, or unresolved trace |
| `RelUndom` | valid exact-set search and no certified dominator | valid certified dominator | missing or invalid search after no dominator is found |
| `CertUndom` | valid search and every relevant pair resolved non-dominating or ineligible | valid certified dominator | any unresolved relevant pair or invalid search |

`Diag` is total on required and report slots. Safety projections retain the
complete selected records, including their witnesses, obstacles, and
provenance. For nonempty required set,

$$
\mu(\mathfrak r)=\bigwedge_{a\in\mathsf{Req}_\beta(P)}\nu_s(e,q,a),
$$

and $\mathsf{Assess}$ maps failed $WF$ to Undefined and the meaningful values
$-,?,+$ to Refused, Withheld, and Granted.

### A.3 Typed elaboration

Detailed records are an elaboration of the same request. An implementation may
represent frames, estimators, routers, proof terms, calibration records,
resource maps, and provenance DAGs as explicit typed fields. Its compression
back to $(s,e,q,P)$ must preserve $WF$, every required and report address, its
$K_3$ value, and its complete transported diagnostic. Under that condition the
elaborated and compact assessments agree. A finite plan DAG is reified as one
$e_G$ only after its typed root payload, grade, and evidence have been
constructed; the internal nodes remain available in its provenance and
certificate.

Object-model output $[e,q]\varphi$, internal derivation
$\Gamma;s\vdash_{VL}J$, external metatheorem $\vdash_{meta}T(VL)$, and accepted
certificate $s\vdash_m\kappa:\mathsf{Claim}$ remain separate through this
elaboration. Only a mode-scoped bridge can turn the last object into its stated
target-world conclusion.

## Appendix B. Proofs and Separating Models for Theorems 1–5

### B.1 Profile refinement

**Proof of Theorem 1.** First prove every generating atom refinement sound for
support. If $U\subseteq\mathsf{Acc}_1\subseteq\mathsf{Acc}_2$, the same region
supports the second adequacy atom. If
$\sup U_e+\Delta_1\leq\inf U_F$ and $\Delta_1\geq\Delta_2$, then
$\sup U_e+\Delta_2\leq\inf U_F$. Constraint-region inclusion is identical to
adequacy inclusion. A trace refinement exists only with a declared projection
that maps every stronger-mode witness to a valid weaker-mode witness. On the
same candidate, scope, criterion, mode, and finite evaluated set, a supported
`CertUndom` record contains a valid search and resolves every relevant pair as
non-dominating or ineligible; its canonical projection therefore supports
`RelUndom`. Identity is sound, and support projections compose along
transitivity.

Suppose $P\succeq_{prof}^{\beta}Q$ and $P$ is Granted. Each required
$b\in\mathsf{Req}_\beta(Q)$ has a required
$a\in\mathsf{Req}_\beta(P)$ with $a\Rightarrow_A b$. Grant of $P$ supports
$a$; atom soundness supports $b$. Hence every required $Q$ atom is supported,
its meet is $+$, and the well-formed $Q$ request is Granted.

For completeness, fix finite address set $\mathcal A$ and the instantiation
fiber $[\beta]_{P,Q}$. Suppose $P\not\succeq_{prof}^{\beta}Q$. Some required
$b$ of $Q$ has no required $P$ antecedent. Define

$$
D=\{c\in\mathcal A:\exists a\in\mathsf{Req}_\beta(P),\ a\Rightarrow_A c\}.
$$

$D$ is downward closed, contains every required $P$ address by identity, and
omits $b$. Independent realizability supplies a finite state in the same fiber
supporting exactly $D$; give every address outside $D$ an explicit open
obstacle. The state grants $P$. It leaves $b$ open and has no refuted required
$Q$ atom, so it withholds $Q$. Thus semantic entailment fails whenever the
syntactic refinement fails. Together with soundness, this proves the
equivalence. $\square$

The independent-fragment condition cannot be deleted. Add a semantic law
$a_1\wedge a_2\models b$ with no corresponding conjunctive syntactic rule.
Then profile $\{a_1,a_2\}$ semantically entails $\{b\}$ although neither atom
refines $b$. The fiber condition also cannot be deleted: alter $q$ or the
evaluated-set field so one profile instantiates to a different address. The
fixed-base separator no longer ranges over that request, and schema-wide
completeness has not been established.

Operational refinement remains separate from target factivity. Use one state
$s$ with an accepted adequacy certificate and pair it with worlds $w_0,w_1$.
Let target risk satisfy the acceptable region only in $w_0$. The same atom is
supported and every profile theorem has the same result in both pairs, while
the unqualified target claim differs. A mode bridge excludes $w_1$ only by an
additional premise.

### B.2 Continuation and stability results

**Proof of Theorem 2.** A stage-local verifier receives isomorphic finite
inputs at $n$ and $n'$, so it accepts the same certificate at both or neither.
If it accepts one, soundness over the declared frame class implies permanent
current stability at $n'$. The assumed descendant with a different assessment
contradicts that implication. Hence no sound scheme accepts at the shared
finite state. $\square$

For deterministic freeze, topologically follow any finite path from $n$. At
the base, the certificate checks $v_a(n)=k$. If the dependency projection and
rule versions agree at one node with those at $n$, the local freeze condition
on the next admitted event preserves them. Induction therefore gives, for
every descendant $m$,

$$
v_a(m)=f_a(\mathsf{dep}_a(m),\mathsf{Rules}_a(m))
=f_a(\mathsf{dep}_a(n),\mathsf{Rules}_a(n))=k.
$$

If this holds for every required atom and $WF$ is preserved, their finite meet
and public assessment are preserved. A current formal proof without the freeze
hypothesis is insufficient: certify normalized cost $9\leq10$, then append an
authenticated correction showing that a unit error makes the cost $12$. The
old derivation remains historical while its current premise lapses or is
rebutted.

For statistical stabilization, choose $N_{cov}$ after which
$\theta\in C_i$ and $N_{diam}$ after which
$\operatorname{diam}(C_i)<\gamma$. Set
$N=\max(N_{cov},N_{diam})$. If $\theta<\epsilon$, then for $i\geq N$,

$$
U_i\leq\theta+\operatorname{diam}(C_i)
<\theta+\gamma=\epsilon,
$$

so every later atom is supported. If $\theta>\epsilon$, then
$L_i\geq\theta-\operatorname{diam}(C_i)>	heta-\gamma=\epsilon$, so every
later atom is refuted. For finitely many required atoms, take the maximum of
their stabilization indices and the eventual $WF$ index. At
$\theta=\epsilon$, intervals may straddle forever, approach from the supported
side, or alternate; shrinking diameter alone gives no conclusion.

For the finite statistical-declaration boundary, suppose
$\mathbb P_-(\tau<\infty,\delta=\text{below})>0$. This event is the countable
union of $E_n=\{\tau=n,\delta=\text{below}\}\in\mathcal F_n$, so some $E_n$
has positive $\mathbb P_-$ probability. Finite-prefix mutual absolute
continuity gives $\mathbb P_+(E_n)>0$, where `below` is the wrong regime.
Interchanging the laws proves the other direction. Thus a procedure cannot be
uniformly zero-error and make finite positive-probability declarations on both
correct sides in this family. This does not preclude high-confidence or
almost-sure eventual correctness under stronger assumptions.

**Proof of Theorem 4.** The `AddDom` witness supplies a descendant $m$ with a
valid dominator and hence $\mathsf{Comp}_e(m)=-$. Since
$\mathsf{Comp}_e(n)=+$, $m$ is a live alternative and permanent stability
fails. Sound certified stability implies permanent stability, so no sound
scheme certifies the positive comparison as permanent. $\square$

The direction cannot be reversed into a polarity-free slogan. If a valid
dominator $d_0$ already refutes the comparison and every continuation preserves
that certificate, then every later comparison remains refuted even as further
plans are added. Similarly, an indefinitely growing archive of plans
inapplicable to $q$ can coexist with a permanently stable
$P_{\mathrm{rely}}$ grant.

### B.3 Footprints, locality, and update graphs

For a fixed request skeleton and slot, the proof uses the following derived
read families. Every row also reads the slot/address, relevant mode and verifier
version, current-validity and correction closure, conflict/priority rule, and
the collection index even when it is empty.

| slot family | additional typed reads |
|---|---|
| `Adeq`, region constraint | certificate and region indices; every indexed certificate and region record |
| `Improve` | the preceding reads for both candidate and named fallback; fallback identity; $\Delta_q$ and comparison order |
| `Trace` | trace index; every indexed trace/countertrace and its current state |
| `RelUndom` | exact evaluated-set index and entries; search index and records; every eligible-pair index and pair record |
| `CertUndom` | all `RelUndom` reads plus current resolution or ineligibility of every relevant pair |
| $WF$ | profile and slots; library membership; plan/interface; context/fallback; referenced versions, modes, units, and comparison view |

An event writes every member it can change and its affected collection index.
Thus an evidence insertion writes the certificate/region index; expiry or
correction writes current validity and correction/index keys; a plan evaluation
writes the exact evaluated-set entry and invalidated search view; and a pair or
search update writes its member and index.

**Proof of Theorem 5.** Equality of slot-instantiation keys first gives the
same address. For a region atom, equality of certificate and region indices
names the same finite records; equality of validity, correction, mode, and
priority data gives the same deterministic normalized region and provenance.
It is therefore missing, conflicted, contained, disjoint, or boundary-crossing
in both states. `Improve` applies the same argument to candidate and fallback
regions and then uses identical margin and order data. Trace equality gives the
same accepted trace, hard countertrace, or open obstacle.

For `RelUndom`, evaluated-set equality gives the same finite set. Search and
pair indices make both present and absent possibilities equal. Normalization
therefore finds the same valid dominators and search validity; the precedence
valid dominator, otherwise valid search, otherwise open yields the same full
diagnostic. `CertUndom` additionally reads every relevant pair resolution, so
its all-resolved test agrees. Each $WF$ obligation is a deterministic query of
the listed keys, hence both states have the same success or the same first
canonical failure. Disjoint diagnostic constructors and deterministic
normalization preserve payload and transported provenance, not only $K_3$.

If $u:s\to s'$ has
$\mathsf{Write}(u)\cap\mathsf{Read}_s(\mathfrak r,i)=\varnothing$, every read
key is unchanged by the event contract, so the projection-equality result
applies. Induction gives the finite-path frame rule with the footprint
recomputed at each pre-state.

Build the canonical graph using every reachable pre-state, with edges event to
written key, key to reading slot, required slot to assessment, and assessment
to grant, including $WF$ edges. If a diagnostic changes along a path, choose
its first changing step. The contrapositive of locality gives a changed read
key, and the event contract says that step wrote it; hence there is an
event–key–slot path. Value, assessment, and grant changes extend the same path.
This proves change-completeness. Path absence therefore implies invariance.
Necessity needs path-realizability: a conservative static edge may be reachable
in the graph even though no admitted event changes the chosen observable.
$\square$

For the phantom separator, begin with an empty pair-record collection and a
valid exact-set search supporting `RelUndom`. If the footprint reads only
existing members, it reads no pair key. Insert the first valid dominator pair;
the atom becomes refuted while every previously read member is unchanged.
Reading `PairIndex` in the empty state and requiring the insertion to write it
restores the event–key–slot path.

## Appendix C. Composition, Routing, and Grounding Proofs

### C.1 Annotated execution and license lifting

**Proof of Theorem 6.** Choose a topological order of the finite plan DAG. At a
source node, totality determines $y_v$ and its declared grade transformer
determines $g_v$. Independently accepted primitive evidence supplies $c_v$.
The plain executor uses the same payload operation, so erasure agrees at the
source.

Assume unique checked bundles have been constructed for every predecessor of
$v$. Type and frame agreement makes the payload transformer defined;
determinism gives one $y_v$ and one $g_v$. The local certificate rule checks
the canonical certificate transformer on the predecessor certificates and
local evidence, while provenance union retains every predecessor source.
Because the annotated and plain executors use the same payload transformer,
erasure commutes at $v$. Induction reaches the root and proves uniqueness,
checking, ordered provenance, and proof erasure.

For license lifting, the accepted root certificate and acceptable grade support
the composite adequacy and named constraint atoms. Every other required atom is
supported by hypothesis. Their finite meet is $+$, and $WF$ excludes
Undefined; hence the root request is Granted. This argument consumes the
composite diagnostic. It never infers a root grant by meeting component grants.
$\square$

The $.06+$.06$ separator is a complete countermodel to unconditional
composition. Give two sequential scalar components independently checked local
error regions bounded by $.06$ and local tolerances $.10$. Let their errors
have the same sign and let the parent grade rule be addition. Each local
adequacy atom is supported, but root error $.12$ is disjoint from the parent
acceptable region $[0,.10]$ and its adequacy atom is refuted. No certificate
transformer can validly certify the false parent bound.

The path-sensitivity constructor is one instance of Theorem 6. At node $v$ use

$$
g_v:\quad b_v=\delta_v+\sum_{u\in\operatorname{pred}(v)}L_{u,v}b_u,
$$

and let its certificate record the local tube, metric, interface, predecessor
certificates, and arithmetic step. Topological construction yields the checked
root path bound; resource maps propagate in parallel under their declared
dimension-specific operators.

### C.2 Grounding and evaluator ranks

**Proof of Theorem 7.** Topologically order the finite support derivation. An
indegree-zero support node is a typed base by hypothesis. At a derived node,
every premise occurs earlier and, by induction, has a path from a typed base.
Adding the declared rule edge gives a base-to-conclusion path; provenance union
preserves the source and rule record. Apply this argument at every supported
required atom.

For the ranked system, every rank-zero evaluator reads only fixed exogenous
inputs, so totality and determinism give a unique output, diagnostic, and
assessment. Assume uniqueness below rank $k$. Each rank-$k$ evaluator reads
only those unique lower-rank values and fixed inputs, so its total deterministic
function has one output. Finite induction reaches the maximum rank. Run the
grounding induction simultaneously: rank-zero support has typed exogenous
bases, and each higher rank preserves their provenance together with its local
sources. $\square$

Acyclicity alone is insufficient: a zero-premise node labelled `supported`
without a typed base is not a derivation from evidence. Grounding alone also
does not establish target factivity. Pair the same grounded meta-state and
system grant with two worlds, one where held-out assumptions transfer and one
with an unrecorded shift. The assessment is the same and target risk differs.
Only a mode-scoped bridge rules out the second pair.

Closed mutual support is excluded from the DAG fragment. For future cyclic
work, a declared ordered space and immediate-consequence operator could admit
one or more fixed points, but existence, selection, and target soundness would
be new obligations. The equations $g=g$ and $g=\neg g$ show why the ordinary
finite core inherits no unique result merely from being written recursively.

### C.3 Routed-risk identity and assumption-finding cases

**Proof of Theorem 8.** The authorized-selection events
$\mathcal G_1,\ldots,\mathcal G_m$, misroute event $\mathcal M$, and fallback
event $\mathcal B$ form a finite measurable partition of the deployment space.
Split the integral of routed loss over this partition:

$$
\int\ell_h\,d\mu=
\sum_j\int_{\mathcal G_j}\ell_j\,d\mu
+\int_{\mathcal M}\ell_h\,d\mu
+\int_{\mathcal B}\ell_F\,d\mu.
$$

On a positive-measure event, each integral is its mass times its conditional
mean; define a zero-measure contribution as zero without assigning a
conditional mean. Substitution gives the exact decomposition. Replacing the
conditional risks by $\epsilon_j,L_M,L_F$ gives the inequality. $\square$

If $\mathcal G_j\subseteq C_j$ and only a whole-cell certificate
$R_{C_j}(\ell_j)\leq\epsilon_j$ is available, nonnegative loss gives

$$
\int_{\mathcal G_j}\ell_j,d\mu
\leq\int_{C_j}\ell_j,d\mu
\leq\mu(C_j)\epsilon_j.
$$

The coefficient cannot generally be replaced by
$\mu(\mathcal G_j)$. Split one cell into equal halves with losses $0$ and $1$,
and select the expert only on the high-loss half. Whole-cell risk is $.5$ and
the actual selected contribution is $.5$, while the naive rescaling gives
$.25$. The broader parent-average separator takes loss $1$ on a set of mass
$.1$ and $0$ elsewhere: parent risk is $.1$ and conditional risk on the bad set
is $1$.

Fallback frequency alone is likewise insufficient. For any small $p>0$, put
fallback or misroute mass $p$ on cases with loss $1/p^2$; its risk contribution
is $1/p$. The explicit gap ensures the selector does not execute an unlicensed
expert, while a bound on deployed task risk still requires a severity or tail
condition. Omitting an uncovered set from all partition cells simply drops its
loss and invalidates the identity.

### C.4 Path sensitivity

**Proof of Theorem 9.** At every node, triangle inequality, the intrinsic error
bound on the reachable perturbation tube, and coordinatewise Lipschitzness give

$$
e_v\leq\delta_v+
\sum_{u\in\operatorname{pred}(v)}L_{u,v}e_u.
$$

Repeatedly substitute this recurrence in topological order. Each intrinsic
error $\delta_u$ reaches root $o$ once for every directed path from $u$ to
$o$, multiplied by the edge factors along that path. Finiteness and acyclicity
make the expansion finite, and collecting coefficients yields
$e_o\leq\sum_uW_{u,o}\delta_u$. If outer loss is $K$-Lipschitz, apply its
pointwise inequality and integrate to obtain the two-sided risk-difference
bound. $\square$

Two assumptions are necessary. If the downstream ideal map is $y\mapsto Ky$,
an upstream error $\delta$ becomes $K\delta$, so unweighted addition fails.
If a downstream implementation is certified only at nominal input $0$ but an
upstream error moves the input to $\delta>0$, the downstream error at
$\delta$ can be arbitrary. Requiring intrinsic and Lipschitz bounds on the
entire reachable perturbation tube blocks this case. Exact bridge-cycle and
resource-accounting results remain in the repository supplement; neither is
needed to derive the main theorem spine.
