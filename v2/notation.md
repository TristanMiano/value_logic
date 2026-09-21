# Phase Two Notation — F01 Bootstrap

Version: September 20, 2026. Authority: the active [queue](../TODO_v2.md).
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
