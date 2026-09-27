# Phase Two Notation — F01 Bootstrap

Version: September 21, 2026. Authority: the active [queue](../TODO_v2.md).
This glossary describes the examples, not a frozen signature for the eventual
calculus. Example-local symbols are scoped explicitly; later tasks should
update this index rather than silently redefine shared terms.

## Shared distinctions

| Term | Meaning in F01 | Not automatically identified with |
|---|---|---|
| value object | information carrying the task-relevant meaning under discussion | one numerical evaluation |
| evaluation | a declared summary or functional used to answer a particular question | metaphysical truth or a universal preference ordering |
| inference | a justified conclusion from stated inputs/assumptions | thresholding an unexplained score |
| context/request $q$ | the operational task, scope, information access, and chosen comparison conditions | an immutable mandatory tuple schema |
| loss/risk $R$ | smaller-is-better discrepancy under a declared criterion | every possible notion of value |
| payoff/benefit | larger-is-better number in a declared unit within an example | probability or a truth degree |
| scenario | an index in a specified example model | direct access to a metaphysical world |
| $\mathbb E$ | explicitly specified finite weighted mean; E07 also gives a declared convergent series | a universally required value functional |
| admissible evaluations | nonempty possibilities relative to accepted example assumptions when nonemptiness is required | an automatically normalized distribution |
| D / L / E / O | derivation / literature / executable work / overhead in the execution protocol | semantic types of the calculus |
| R / X lane | reliable / exploratory research effort, in timing records only | task risk $R$ or payoff $X$ |

## Example-local symbols

| Scope | Symbols and conventions |
|---|---|
| E01 | $f(z)=z+z^3$ is the declared benchmark; $M_c,M_a$ are cheap/accurate models; $a>0$ sets $D_a=\{-a,a\}$; $c_M$ is work cost; $\epsilon$ is error tolerance; $b$ is work budget; $\lambda$ converts work units to loss units; $J_q=R_a+\lambda c$ is this example's comparison, not a global value definition. |
| E02 | $A,B$ are two-output models; $e_i$ are comparable error components; $\theta\in[0,1]$ selects task importance; $R_\theta=\theta e_1+(1-\theta)e_2$. |
| E03 | $X,Y,Y'$ are jointly indexed two-scenario payoffs; minimum/maximum are pointwise operations; the requested evaluation is applied afterward. $t$ in section 10.1 is a joint-cell probability, not time. |
| E04 | $f,g$ are reference stages; hats indicate approximations; $\delta$ is an upstream error bound, $\eta$ a downstream error bound on perturbed reachable inputs, and $K$ a downstream Lipschitz coefficient with the appropriate unit conversion. |
| E05 | $S_{\rm precise},S_{\rm uncertain},S_A,S_B$ are sets of admissible numerical evaluations or source assertions for one scoped quantity. Empty compatibility is different from nonempty uncertainty. |
| E06 | $T_2,T_3$ are finite equational presentations with stated interpretations; $N\in\{0,\ldots,5\}$ is uniform; $M_k$ returns only $N\bmod k$; $P,Q$ name parity and residue-three tasks, not probabilities. |
| E07 | $h(x)=x/(1+|x|)$ is an exact recoding; $h^{-1}(y)=y/(1-|y|)$ on $(-1,1)$; $\oplus_h$ transports addition. Its local $a,b$ are encoded inputs, not E01's amplitude/budget. Precision $\eta$ is local to that encoded-output contract. The later $X(k)=k$, $Y(k)=2$, and $p_k=2^{-k}$ form an infinite-scenario example. |
| E08 | $S_{\rm obs}$ is a binary signal; $p$ is symmetric accuracy; $\kappa$ is acquisition cost in payoff units; the admissible action policy may depend on the signal only after acquisition. |
| Section 10 | $P_+,P_-$ are joint probability tables; $U,V,W$ are binary payoffs in the three-way dependence test. These are not the formal systems $T_k$ or an adopted general value carrier. |

Bounds and units belong to their stated example. Inequalities use ordinary
real order in the declared metatheory. No universal conjunction/disjunction,
consequence relation, context type, or boundedness axiom has been introduced.


## Reconstruction-note symbols and contracts

These symbols belong to the [F01 reconstruction note](foundations/01a_reconstruction_and_information_contracts.md),
not a new global signature.

| Scope | Symbols and assumptions |
|---|---|
| B | Binary supports `a<b`, `c<d`; `alpha`, `beta` are upper-atom probabilities and `t` is a joint-cell mass. In the separate ternary example, `P_c` is a symmetric joint table. Support and moments are in fixed dimensionless payoff coordinates; covariance zero is not independence. |
| B.3-B.4 | `D=X-Y` is a payoff difference, not a timing mode. The weakened moment-only answer range has an unattained upper endpoint. A closed hull, the actual answer set, and a uniform strict margin are distinct objects. |
| C | `n` is number of binary payoffs; `P_0/P_1` are even/odd parity laws; `M>=0` scales payoffs. The marginal-interaction bound is an integer `r>=1`, not a bound on arbitrary encodings. |
| D | `C,F` are candidate/fallback losses; `z` is a shared unknown; `S` is a nonempty finite joint set. The co-attainment criterion uses attained extrema. |
| E | `h` is the recoding from E07; a finite decoded range `[0,M]` and a code-error radius must be supplied together. Exact recoding differs from using ordinary arithmetic on codes. |
| F | `s(z)` is a summary, `psi(z)` its queried numerical answer, and `Z_c` the compatible nonempty fiber. `A_epsilon(theta)` contains epsilon-optimal actions in model theta. Regret is a declared diagnostic, not a universal primitive. `alpha_a` denotes a failure-probability bound; simultaneous coverage is a separate event. |
| G-H | `p(w,s)` is a joint state/signal law; `V_0,V_S,V_*` mean no-observation, signal-policy, and hidden-state-oracle values. For one conditioning event, `b=E[X 1_A]`, `p=Pr(A)>0`; raw moments and estimated moments are separate. |
| I | `e_i` are binary violation indicators, `r_i=E[e_i]` exact probabilities, and `epsilon_i` upper caps. `w_i,t` are mixture weights for single/triple violations. Existence of a fitting joint law is not a universal guarantee over laws or empirical calibration. |
| J | Uniform error, mean absolute error, and error of the mean are different quantities. `K(w)` is a local sensitivity and `delta(w)` an error profile; their joint mean product differs from the product of their means. |
| K | `N` is the revealed-prefix length, `L_M` a loss with a hidden tail spike, and `Ck` a supported envelope. Individual integrability does not imply a common expectation bound across models. |


## F02 candidate-local notation

See [the candidate comparison](foundations/02_candidate_semantics.md). These
symbols do not replace the example-local F01 conventions or freeze a signature.

| Scope | Meaning and important distinction |
|---|---|
| S | `s_q(e)` is a finite real payoff at a fixed task `q` and unit `u`; an interval bounds an evaluated scalar, not a per-scenario distribution. |
| P | `x in R_u^Omega` is a shared-index profile; `V_p(x)` is its specified weighted mean. Model index `theta` is shared across components when stated. |
| T | `T: R_u^B -> R_u^A` maps a downstream continuation to input-state values; primitive `T_(r,P)(h)=r+Ph` uses a row-stochastic matrix P, distinct from the candidate label P. |
| T sequencing | `(T;U)(h)=T(U(h))` describes T running first. Min/max require an explicitly declared controller/adversary and observation stage. The extensional map does not automatically retain the generator syntax or policy witnesses. |
| T test family | `osc(h)=max(h)-min(h)`; `H_M` contains all continuations of span at most M, with unbounded common shifts. `TV(p,q)=sum(abs(p-q))/2`. |
| G | For a finite menu A of d-component smaller-is-better costs, `Gamma_A={b: exists a in A, a<=b}`. Capability order is set inclusion, not a weighted total ranking. |
| G composition | Menu union is controlled choice; pairwise cost addition requires freely compatible uses. Typed triples `(x,c,y)` compose by matching endpoints and adding costs. |
| G robust extension | `cbar_j(a)=max_theta c_j(a,theta)` answers the specified universal component-cap query with one action chosen before theta is observed; it need not preserve later sum objectives. |

The candidate label S is not a signal variable or an evidence set, and the
candidate label G is not a particular program step. Context determines these
notations. Common unit conversions, allowed task families, and information
schedules must be stated wherever the corresponding operation is used.


## F02 S2 supplement: scoped symbols, not a permanent signature

The [candidate reconstruction](foundations/02a_candidate_reconstruction.md)
uses the following local conventions in addition to the F02 S1 glossary.

| Scope | Symbols and meaning |
|---|---|
| A, J | Nonempty finite cost menu `A`, upper budget set `Gamma_A=A+R_+^d`, convex upper hull `C_A=conv(A)+R_+^d`, and weighted optimum `f_A(w)=min_a w.a`. Nonnegative weights are declared task conversions. Per-use budgets differ from expected-budget mixtures. |
| B | Blind choice is before the input is known; observed choice can depend on the supplied input. Equality of optimized maps is not equality of legal menus under a different information schedule. |
| C | `osc(h)=max h-min h`, relative-stake bound `M`, stochastic rows `p_a`, immediate rewards `r_a`, and exact output-span allowance `B_U(M)`. These are candidate T assumptions, not universal value axioms. |
| D | Positive scenario weights `p_i`, profile masks `q^(i)`, and bounds `L,U` defining admitted probes. Exact profile recovery is query-relative, not a real-coordinate counting lower bound. |
| E, F | Separate-feasibility intersection permits different witnesses. Shared-model index `theta`, suffix lower envelope `k`, prefix value `c_theta`, and nonnegative gap `g_theta` govern the early-reduction equality criterion. |
| G | Cost-labelled endpoint relation `R`, backward budget transformer `W_R`, and fixed-weight min-plus endpoint cost kernel `K^w`. Empty continuation sets have no feasible witness. Nonlinear budget probes require a richer output interface. |
| I | Finite continuous piecewise-affine maps, stochastic affine pieces, max-min normal form; exact equality is extensional. Smooth comparison `F_*(h)=log((exp(h_1)+exp(h_2))/2)` and its tangent/intercept constructions are analytic fixtures. The 65-plane approximation has exact rational coefficients. |
| J | Positive component scales `s_j` and directed slack `d_s(A,B)=max_a min_b max_j((b_j-a_j)/s_j)_+`. Convexified slack `d_s^cvx` answers the relaxed expected-budget question, not the hard deterministic question. |
| K | Anchored relative-stake polytope and joint affine-region refinement; Boolean or original box vertices alone need not determine nonlinear T comparisons. |
| L | `phi(x)=x/(1+abs(x))`, common offset `c=h_n`, relative coordinates `d=h-c1`, code radius `eta`, decoded radius `delta`. Centering precedes rounding; preserving offsets is necessary for absolute outputs. |
| N | Shared signal model: hidden state `W`, cheap signal `S_C`, menu error/work pairs `(1/2,0),(1/4,1),(0,3)`, work price `lambda`, and independently declared error/work caps. |

All guarantees are relative to the displayed finite or explicitly extended
models. A resource frontier does not infer physical prediction error without
an error-propagation premise. No new universal conjunction, context schema,
probability semantics or boundedness requirement is introduced by this table.


## F05 provisional notation (S1; not a permanent signature)

| Notation | Current meaning and restriction |
|---|---|
| Sigma | Finite versioned source signature, units and named positive rational conversions. |
| x_u; y_u | Source coordinate and lexical local, respectively; different namespaces. |
| t_u | Finite rational CPWA loss term in unit u. Pointwise values are finite; global ranges may be unbounded. |
| res(a,b) | max(b-a,0), a derived nonnegative deterioration operation. |
| C; D_C(o) | Evidence context and its finite union of nonempty rational source polyhedra at visible observation o. |
| h; x | Hidden interpretation case and its source assignment; neither is policy-visible by default. |
| C |= t <=_b s : u | For every admitted case and assignment, new t minus old s is <= the signed budget b. |
| B_C(t,s) | Supremum of the signed difference, in R union {+infinity}; a metalevel target, not an oracle term. |
| S_C(t,s) | max(B_C(t,s),0); equivalent budget test only for b>=0. |
| pi:O->program/lottery | Finite visible-information policy; proof case splitting cannot reveal h. |
| phi:D_new->D_old | Source-meaning/domain map needed for evidence transport; typing alone is insufficient. |
| H_r; L_r; J_r | Controller failure probability, proxy expected cost, and intended modeled cost, respectively. |
| e; beta | Paired intended/proxy discrepancy and its upper bound for the named old/new policies. |
| q; U4 | Abstract expected-event source and four-cell CPWA upper enclosure for theta^2; not an exact multiplication operator. |

See [the core](foundations/03_provisional_core.md) and
[reconstruction](foundations/03a_semantic_reconstruction.md) for assumptions.
There is no introduced general proof-theoretic relation |- yet; selecting rules
and proving them sound remain F06 and F07 obligations. A pointwise audit result
must not be labelled universal validity or empirical confidence.


## F05 completion additions: observations and relative evaluation

Use the [core](foundations/03_provisional_core.md) and [S2 audit](foundations/03b_observation_and_revision_audit.md)
for scope; these are optional views of the existing semantic objects.

| Symbol | Meaning and condition |
|---|---|
| `J_a(o,h,x)` | Declared cost of the same versioned action `a` in a visible observation `o`, hidden case `h` and source assignment `x`; all available actions need interpretations. |
| `pi(o)` | A fixed normalized rational action lottery chosen from visible `o`, not hidden `h` or unobserved `x`. |
| `d_a=J_a-J_a0` | Relative-cost image for a fixed action library/reference and same-unit comparisons. Preserves normalized-lottery contrasts, not absolute cost. |
| `span(e)=max_a e_a-min_a e_a` | Sharp all-lottery contrast-error seminorm; a common offset is ignored. Units must agree. |
| `TV(pi,pi')=sum_a abs(pi_a-pi'_a)/2` | Policy mass moved. A fixed contrast error is at most `TV*span(e)`. |
| `Q=sum_i q_i res(r_i,H_i)` | Positive expected report shortfall. `Q=0` means every positive-weight emitted report is valid in that interpretation. Not `res(sum q_i r_i,sum q_i H_i)`. |
| `a(d)=inf {y:(d,y) in S}` | Optional lower-fibre summary for specifically upper-threshold evidence; finite infima attained under the stated rational-polyhedral conditions. Not a summary for arbitrary future filters. |

Log loss, Brier design optimization and infima are used in the external semantic
adapter proofs. They are not quietly added to the finite native term grammar.


## F06 first-pass notation

`C;h |- t <=[b] s:u` is a supplied-rule derivation of the signed comparison
`t-s<=b` in live case h; `|=` remains the independently specified F05 meaning.
Omitting h denotes exhaustive hidden-case coverage for a fixed policy.
`beta_pi(eta)` is one proof's calculated budget as a function of finite row
bounds, with fixed row directions/scope/case schema. It is not the modeled cost,
a confidence probability, a universal optimum or an unexplained truth degree.
`k>=0` in a weakening node is a fixed added slack, not an unchecked fixed target.
Source-dependent rewrites, changed criteria, missing rows and policy changes
need separate obligations. Nonlinear terms are compared by the stated rules;
normalization alone handles only its explicit identities. See
[the rule register](derivations/02_inference_rules.md).


## F06 S2 notation — source transport and assumption discharge

* `sigma`: a closed, typed substitution from old source keys to new terms; its
  numeric pullback is distinct from a checked observation/policy translator.
* `P|h`: a localized finite proof for one live case; its budget may be stronger
  than an old all-cases maximum.
* `(S,b)`: at one fixed evidence snapshot, a sufficient row-support set and its
  scalar proof bound. Row identities are relative to the context fingerprint.
* `v_i=res(eta_i,a_i)`: nonnegative magnitude of a numerical row's violation.
* `e_P(x)`: the symbolic allowance emitted by a local discharged proof, using
  the ordinary judgment `t <=[0] s+e_P`. This is not a scalar budget oracle.
* `P_P=e_P-b_local`: a nonnegative deterioration allowance when rows are only
  softened from the localized original bounds.
* `tau`: a separately warranted observation translator; numeric substitution
  alone does not establish `O(sigma(y))=tau(O'(y))`.

Availability, actual premise validity, numerical violation and probability of
coverage are distinct. No native positive/negative-infinity arithmetic is added.
