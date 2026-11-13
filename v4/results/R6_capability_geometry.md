# R6.7 Diverse values identify attainable capabilities

**Contributor:** Codex (GPT-6), November 12, 2026.
**Cycle:** [P4-R6-C001](../notebook/P4-R6-C001/record.md), cycle complete; module available to recur.
**Evidence:** a synthesis of established convex decision geometry, statistical
experiment comparison and policy transfer, with self-contained finite proofs
and exact examples. No priority claim is made for the component theorems.

A family of values can describe an agent's capabilities precisely: it says
how well the agent can do under each goal. When the goals cover enough
directions, this description determines the attainable outcome geometry.
Information and options are two ways to enlarge that geometry. Their shared
instrumental value therefore has one mathematical explanation.

This advances a faithful part of C7 and connects W6 to C1/C2's recovery of
task distinctions. It describes attainable behavior, rather than the details
of the code implementing it. The companion
[policy reconstruction](R6_policy_values.md) treats the author's proposal to
recover a particular policy from conditional trajectory counts.

## 1. Capability as a family of attainable outcome vectors

Fix the environment, initial condition, resource budget and allowed policy
class. Each policy produces an expected vector z of outcome features. These
may be terminal outcome probabilities or discounted feature totals. Assume
the vectors are bounded. Let K be their closed convex hull: randomization
between policies is allowed, and limits are included for this description.

A goal is a linear payoff vector w. Its best attainable value is

```math
V_K(w)=\max_{z\in K}\langle w,z\rangle=h_K(w).          \tag{C.1}
```

This is the support function of K. Listed actions that are redundant inside
the same convex hull do not create additional capability in this model.
Changing the action labels or controller implementation can leave K unchanged.

**Theorem 1 (capability/value duality at an explicit quotient).** For
nonempty compact convex sets K and L in a finite-dimensional Euclidean space:

```math
K\subseteq L\quad\Longleftrightarrow\quad
V_K(w)\le V_L(w)\ \hbox{for every }w.                    \tag{C.2}
```

In particular, their whole value families are equal exactly when K=L.

*Proof.* Inclusion immediately implies the value inequalities. Conversely,
if x in K lies outside L, strict separation of a point from a closed convex
set gives a direction w with w*x greater than max over L of w*z. Then V_K(w)
exceeds V_L(w), contradicting the assumed inequalities. QED.

The relevant equality is on **attainable outcome geometry**. It does not
identify a unique implementation, intrinsic reward or belief/preference split.
Those are different inverse problems. This quotient preserves the operational
content: which goal-conditioned decisions the agent can successfully realize.

## 2. Approximate values give approximate capability recovery

Let d_H denote Euclidean Hausdorff distance, the smallest epsilon such that
each set lies within epsilon of the other. Then the standard support identity
is

```math
d_H(K,L)=\sup_{\|w\|_2=1}|V_K(w)-V_L(w)|.              \tag{C.3}
```

*Proof.* If each point of K is within epsilon of L, maximizing its inner
product with a unit vector gives V_K<=V_L+epsilon; reverse the sets for the
other inequality. Conversely, V_K<=V_L+epsilon on the unit sphere extends by
homogeneity to every direction. The support function of L+epsilon*B is
V_L(w)+epsilon*||w||, where B is the unit ball. Theorem 1 gives K contained
in L+epsilon*B, and the reverse inequality gives the reverse containment.
Taking the least epsilon proves the identity. QED.

For a finite delta-net of unit directions {w_j}, suppose K and L lie within
radius R of the origin and their queried values differ by at most epsilon.
Each support function is R-Lipschitz in w. Choosing a net direction within
delta of any w yields

```math
d_H(K,L)\le\epsilon+2R\delta.                           \tag{C.4}
```

If both sets fit noisy observations within eta at those directions, use
epsilon=2*eta. These are deterministic coverage bounds; they do not supply
the observations for free. Statistical reconstruction of convex bodies from
noisy support measurements is established, substantially more developed work;
see [Gardner, Kiderlen and Milanfar (2006), sections 2 and 6](https://arxiv.org/abs/math/0608011).
The limited comparison here uses their geometric setting, not their stronger
Gaussian estimation rates.

If goals cover only a subset W, the identified object is instead the
equivalence class under equality of V on W. For example, nonnegative weights
observe the upper supported frontier and need not identify the whole hull.
Full signed directional coverage can be represented using both each feature
and its negative, if those additional uses are actually available. Positive
rescaling alone cannot turn an arbitrary signed weight into a nonnegative one.

There is an important constructive exception. If every attainable vector has
the same known total $\langle\mathbf 1,z\rangle=m$, choose $b$ so that
$w+b\mathbf 1$ is strictly positive, and let
$a=\sum_i(w_i+b)>0$. Then

```math
h_K(w)=a\,h_K\!\left(\frac{w+b\mathbf 1}{a}\right)-bm. \tag{C.4a}
```

*Proof.* Adding $b$ to every weight adds the same $bm$ to every feasible
payoff; positive rescaling multiplies every payoff by $a$. Maximizers and
the displayed identity follow directly. QED.

Thus values on the nonnegative simplex **do identify the full hull on a
known fixed-total hyperplane**. Terminal-outcome distributions and normalized
discounted state occupancies have total one, so this applies to them. General
feature totals need not have fixed total. For example, $K=[0,1]$ and $L=\{1\}$
agree for every nonnegative scalar weight, but $h_K(-1)=0\ne-1=h_L(-1)$.
The fixed-total condition characterizes when an additive baseline is a
harmless recoding of a goal and when it changes the practical question.

## 3. Information is a capability enlargement in the same geometry

Let theta be a finite hidden world state with full-support prior mu. An
experiment E gives a finite signal s with probability E(s|theta). For a finite
action set A, a policy pi(a|s) induces the joint world/action law

```math
z_{\theta a}=\mu_\theta\sum_s E(s\mid\theta)\pi(a\mid s).
                                                               \tag{C.5}
```

Let K_E(A) be the compact convex set of all such laws. For any actual payoff
u(theta,a), optimal expected performance is h_{K_E(A)}(u). Observation has
enlarged the agent's attainable *contingencies*: it can choose differently
in different states without controlling the state itself.

**Theorem 2 (finite experiment comparison).** The following are equivalent:

1. F can be obtained by a stochastic garbling T of E: F=ET.
2. K_F(A) is contained in K_E(A) for every finite action set A.
3. E has at least as high optimal expected value as F for every finite A and
   every payoff table u, under the stated full-support prior.

*Proof.* For 1=>2, an E-policy can first sample the garbled signal using T
and then execute any F-policy. For 2=>3, apply Theorem 1. Conversely, 3 and
Theorem 1 imply inclusion for the particular action set consisting of F's
signal labels. The F-policy that reports its own signal attains
z(theta,a)=mu_theta*F(a|theta). Inclusion supplies an E-policy T(a|s) attaining
this same vector. Divide by the positive prior coordinates to obtain F=ET.
QED.

This is the finite Blackwell experiment order, expressed in the same
attainable-law language as options. The proof is reconstructed here; the
original [1951 record](https://digicoll.lib.berkeley.edu/record/112749) was
located but its scan was inaccessible in this cycle. No fresh full-source
review of that scan is claimed. The result is also a useful bridge back to
[R6.1](R6_goal_judgment.md): retaining a context distinction is valuable when
the goal family exposes a contingency that losing it would remove.

For an explicit check, take a fair binary world, an E-signal with error 0.2,
and an F-signal with error 0.35. Independently flipping E's report with
probability 0.25 gives F. The checker evaluates all 81 payoff tables with
entries in {-1,0,1}; each satisfies the predicted value ordering. Reversing
the names of E's signals preserves its capability set and all values.

The same argument does not make information acquisition free. If acquiring
E costs resources or changes which actions remain feasible, the comparison
must use those altered attainable sets. [R6.3](R6_shared_observation.md)
provides one explicit funding and reuse boundary.

## 4. A concrete description-complexity consequence

Let b be an arbitrary d-bit capability vector and

```math
K_b=\mathrm{conv}\bigl(\{0\}\cup\{e_i:b_i=1\}\bigr).
                                                               \tag{C.6}
```

The agent can either do nothing or produce one available unit outcome. Its
value for goal e_i is exactly b_i. Suppose a stored representation, with a
fixed decoder and no uncounted access to b, answers all these value queries
with absolute error strictly below 1/2. Thresholding its answers recovers b.
Therefore different b require different representations: a fixed-width
representation needs at least d bits in the worst case.

This is an elementary counting lower bound, not a new complexity theorem.
It makes the C7 reading concrete: **a value representation sufficient for
separating practical uses must retain their behaviorally relevant capability
information**. A representation answering only the first goal needs only b_1;
the other bits need not be retained. Simple rules can also describe structured
families compactly. The number of states alone is not a lower bound on the
shortest program, and this argument proves no general computational-time
equivalence between evaluating a value and executing a controller.

## 5. Established constructive alternatives

Successor features give the sequential version of the linear pairing: for a
fixed transition system and policy pi, the expected discounted feature vector
psi^pi(s,a) satisfies Q_w^pi(s,a)=psi^pi(s,a)*w. It can be reused when rewards
change. [Barreto et al. (2017)](https://me.net.nz/files/publications/barreto2017sf.pdf)
combine such evaluations through generalized policy improvement. With exact
values, their resulting policy performs at least as well as every policy in
the supplied bank; their approximate theorem quantifies the evaluation error.

[Alegre, Bazzan and da Silva (2022)](https://arxiv.org/abs/2206.11326)
go further by constructing a policy set whose successor features cover the
declared linear reward family, giving optimal transfer at the stated coverage
scope. Their working weight set is a nonnegative simplex. It should not be
silently substituted for all signed directions in (C.2)--(C.4).
For their state-occupancy application, however, the fixed-total repair
(C.4a) does justify recovering all signed preferences. The general reward
feature case requires checking this condition or explicitly retaining signed
features. Their Theorem 3.2 follows because the bank contains an optimal
policy for each covered weight and GPI weakly improves every member. Their
Theorem 3.5 combines the bank's coverage error with a nearest-weight
transfer bound. These are stronger constructive algorithmic guarantees than
the present identification argument.

These methods are strong practical alternatives to rebuilding a learner for
every new purpose. The present result organizes why reusable information and
options help different goals, and what value observations identify. It does
not claim a superior transfer algorithm. Extending this geometry to learned,
budget-limited, changing ontologies is a substantive remaining obligation.

The [checker](../notebook/P4-R6-C001/capability_geometry.py) gives exact finite
information and capability-code examples. Theorems 1--2 and bounds (C.3)--(C.4)
are mathematical arguments, not inferred from that finite enumeration.
