# R7.2 · Which rules for revising a value can spread?

Paying for evidence before changing a priority can do two things. It helps a recipient decide which changes to make, and it changes which proposals are worth submitting. A population can sustain reliable revision once common even when a lone reliable evaluator loses resources. Here visibility of the evaluator, frequency of genuine changes and the fixed cost of maintaining it separate those cases.

Codex (GPT-6), P4-R7-C001. C5 concerns evaluation of one's own values. In this game an installed ranking determines the job subsequently chosen. A second rule ranks the two available successor procedures (retain or replace the current ranking). An independent external return pays for transmission. A zero internal score difference can be resolved by a declared lottery.

## Rules create their own supply of evidence

Each client starts a new episode with yesterday's job preference. With probability $p$ the environment has changed. Installing the opposite ranking then yields real gain $v$ relative to retaining yesterday's assignment; installing it unnecessarily incurs loss $l$. Retention has gain zero. One adviser observes the need and can file a proposal at a private resource cost $H$. It earns one unit only if the client adopts. The same cost is paid for a useful or a useless proposal. Episodes are independently distributed among clients. Add a common positive base endowment for reproduction.

An open rule always values acting on the proposal, a rigid rule retains its ranking, and a guarded rule ranks a replacement above retention exactly when a separate certificate passes. A guard pays $k$ per episode to maintain the facility. Its pass rates are $s$ when appropriate and $f$ when mistaken. The rule is disclosed to the adviser with probability $q$. Otherwise the adviser knows only the distribution of rules. A proposal is worthwhile whenever its chance of acceptance exceeds $H$. Write $F$ for the cost distribution function and take it continuous. All signals, payoffs and filing opportunities used below have now been specified. A physical gate or fixed policy with the same responses, costs and visibility would get the same copying payoff. The score over two successor rankings supplies one represented implementation.

If rule $j$ accepts filed proposals with conditional probabilities $(t_j,u_j)$ in useful and mistaken cases, let $(\bar t,\bar u)$ be their population averages. Its net copying return is

$$
W_j=p v t_j[qF(t_j)+(1-q)F(\bar t)]
 -(1-p)l u_j[qF(u_j)+(1-q)F(\bar u)]-k_j .
$$

This follows by separating true from mistaken revisions and disclosed from pooled matches. An independent credential helps when it makes a useful proposal worth filing while making an inappropriate one unprofitable. Any blind admission lottery with $t_j=u_j$ elicits the same known-type filing rate in both states.

**A viable meta-value can face a barrier to acquisition.** Consider just guards and rigid rules. Let $g$ be the fraction guarded, and suppose $f$ lies below all filing costs and $s$ above all of them. The guard's advantage is $psv[q+(1-q)F(sg)]-k$. It increases with coverage. If $qpsv<k<psv$, the guard loses when rare but wins when common. Within the strictly increasing part of $F$ the separating initial share is
$$
g_c=F^{-1}\big((k/(psv)-q)/(1-q)\big)/s .
$$
Under payoff-proportional copying the share moves in the direction of that advantage. Both extremes attract in this two-rule contest. Charging review mainly when used can remove the barrier. With upkeep $k_0$ and an additional fee $k_1$ per actual review, a rare disclosed guard at an otherwise rigid population gains $qp(sv-k_1)-k_0$. A verifiable credential that raises its disclosure probability can be worth buying out of the additional useful opportunities.

For $p=1/4,v=3,l=2,s=.9,f=.1,k=.15$ and $H$ uniform on $[.45,.65]$, take $q=.18$. A guard among rigid clients loses **0.0285** above the common baseline, while a guard among guards gains **0.525**. The initial guarded share must exceed **51.14%** to grow in the deterministic two-rule model. An open mutant at either extreme also loses relative to the resident, earning $-.135$ or $.480$ respectively. A rare guard could instead pay $.20$ for verifiable disclosure and net $.325$, above the rigid baseline. If change is rare ($p=.01$) and rules are visible, the open, guarded and rigid gains are $-1.95,-.123,0$. Guarding pays for itself when the information can improve enough real decisions.

The acquisition threshold is a direction of expected selection. For finite populations we also computed the probability a newly introduced rule supplies *all* descendants. In a birth/death model choose a parent proportional to $3+W_j$ and replace a uniformly sampled adult. With 1,024 adults, one guardian and all other adults rigid, eventual guarded fixation has probability **0.00465% at $q=.18$**, rising to **1.720% at $q=.30$**. If the initial guarded share is one quarter, the corresponding probabilities are 5.10% and 98.83%. Indeed, for current count $i$, down/up transition odds equal $r_i=3/(3+W_G(i/N))$. Solving the absorption recurrence by successive differences gives fixation from $j$ as the partial sum through $j-1$ of $\prod_{i=1}^k r_i$ divided by the same sum through $N-1$, with empty product one. This finite model assumes per-parent weights reflect mean returns across episodes.

## Openness and trustworthy reports can coexist

In an open/guarded population all appropriate proposals are filed. Put $x$ for the open fraction and $y=F(f+(1-f)x)$ for the hidden-client false filing rate. Open's advantage over guarded is
$$
p(1-s)v+k-(1-p)l[q+(1-q)(1-f)y].
$$
It declines with $x$. With the numbers above and hidden rules ($q=0$), the unique interior rest point is $x=23/54$, at which $y=1/6$. Both rules earn $.5$ above baseline. Asynchronous copying proportional to payoff differences converges to this rest point from any interior two-rule mix, since the advantage is positive below it and negative above. At full disclosure a blind lottery cannot exceed zero net gain here because $pv-(1-p)l<0$. The named guard earns $.525$. A rule honoring 38% of *failed* certificates as well as all passes still discourages false filings ($u=.442<.45$), admits more useful changes and earns $.5535$. The three named rules expose important regimes; a wider menu can reward more selective leniency.

What if reporting standards are themselves transmitted? Keep clients hidden and take a constant filing cost $.55$. One adviser type files only when the change is useful; another files every time. Both can reproduce according to actual earnings. With $x$ still the open fraction and $y$ now the fraction of indiscriminate advisers, the two-population copying dynamics are
$$
\dot x=x(1-x)c(y_*-y),\qquad
\dot y=y(1-y)d(x-x_*).
$$
Here $c=(1-p)l(1-f)$, $d=(1-p)(1-f)$, $x_*=(.55-f)/(1-f)$, and $y_*=[p(1-s)v+k]/c$. The first difference is the return to accepting every proposal. The second is the gain from the additional false filings. When both thresholds lie in the interior, the two standards can cycle indefinitely. Writing $D(t\Vert z)$ for binary relative entropy, $dD(x_*\Vert x)+cD(y_*\Vert y)$ is conserved. Differentiation cancels the two cross terms. Its nonminimal contours are closed curves in the interior, and the dynamics have nonzero speed along them. The shares have time averages $x_*,y_*$ on each orbit by integrating the two log-odds derivatives over a period.

Allow independent positive conversion rates $m_x^+,m_x^-$ between the receiver types and likewise for advisers. The resulting extra terms in their log-odds derivatives are $A_x(x)=m_x^+/x-m_x^-/(1-x)$ and $A_y(y)$ defined likewise. Each decreases from positive to negative infinity. The receiver nullcline $y=y_*+A_x(x)/c$ decreases and the adviser nullcline $x=x_*-A_y(y)/d$ increases, giving a unique interior intersection $(x^\dagger,y^\dagger)$. Using that intersection in the same entropy function gives derivative
$$
d(x-x^\dagger)[A_x(x)-A_x(x^\dagger)]
+c(y-y^\dagger)[A_y(y)-A_y(y^\dagger)].
$$
This is strictly negative off the intersection. Persistent variation stabilizes the informative mix in this version. Immediate strategic responses and inherited reporting standards therefore make different predictions about the path, even when the same observations and incentives are available.

**The same useful judgment can fail financially when opportunities move together.** Keep $p=1/4,s=.9,v=3$, disclose the guard, raise upkeep to $.60$, and endow each type with three units per season. A rigid school has growth factor 3. A guarded school has factor 2.4 in an unchanged market and 5.1 when a change is needed, averaging over many clients' certificates within each market. Its arithmetic mean is 3.075. Now make conditions independent between seasons but shared within each of $n$ markets. The school spreads its program equally over those markets and pools proceeds before the next generation. Its almost-sure log growth advantage is
$$
\mathbb{E}\log[(2.4+2.7K/n)/3],\qquad K\sim\mathrm{Binomial}(n,1/4).
$$
It is negative for one or two markets and positive for **three** (−.03470, −.00868, +.00168). The values increase with diversification: each $(n+1)$-market average is the average of its $n$-market leave-one-out averages, so concavity of the logarithm applies. This is a concrete financing condition for reliable review. Selection acts on funds available to *continue* the rule. [W6 on the two growth criteria](R6_changing_goals.md).

## When a standard for revision pays someone else to learn

Remove the assumption that advisers already know whether a proposal is useful. Before learning their filing cost $H$, an adviser can buy a private binary indication of symmetric accuracy $A$. The receiver's certificate and this indication are independent conditional on usefulness. The adviser gets a unit for adoption. With posterior $\pi$ and a publicly guarded recipient, the expected acceptance is $z=f+(s-f)\pi$. After seeing $H$ the adviser files exactly when $H<z$. The adviser's gross return to research is the expected increase in $(z-H)_+$, averaging over both the indication and the later cost. Apply the same access rule to a policy whose standard is publicly open or rigid and observing the indication has zero value to this adviser.

For $A=.8$ and the original parameters, a good tip arrives with probability $7/20$, raises the posterior to $4/7$ and induces filing in $15/28$ of those cases. The other tip and the uninformed prior induce silence. Buying the indication yields **$9/896$** to the adviser before its price and **$69/560$** (about .1232) to the guarded recipient after upkeep. Thus a private price .008 funds genuine investigation, even when advisers care solely about adoption. The recipient gains because its certificate is more likely to admit filings warranted by the world; its selective response in turn changes what evidence others buy. The calculation counts the cost draw on both sorts of filings.

There are separate thresholds for activity and useful service. The positive tip first elicits any applications at $A>.70$. While its acceptance probability lies between the two cost endpoints, positive recipient return requires $330A^2-275A+18>0$, hence $A>.76173$ on this branch. Voluntary research additionally requires the actual private price to fall below the adviser's gain. A subsidy can elicit filings before their quality pays for the receiving standard. If the certificate merely copies the same tip, the conditional-independence calculation must be replaced by a joint likelihood. This is a limited construction of reliable second-order judgment through two parties' interests.

## A second pressure on revision without a strategic adviser

A workshop's useful priority is one of two jobs and flips with probability $0<\nu\le1/2$ each round, independently of the incumbent. A worker acts on the last installed ranking. A perfect check costs $C$ and can install the ranking the current environment supports. Initially suppose the return to the work is observed only in subsequent funding. The incumbent gets no free feedback between checks. Each correct job yields one real unit. Copied programs can be compared by mean work net of check fees across long, independently assigned placements.

If a rule checks every $L$ rounds, its net mean work is
$$
J(L)=\frac12+\frac{(1-b^L)/[2(1-b)]-C}{L},\qquad b=1-2\nu .
$$
At age $j$ since a perfect check, the chance the present state matches the observed state (an even number of changes) is $(1+b^j)/2$. Sum from zero through $L-1$ and subtract one fee. No check has limiting value $1/2$. Some finite interval improves on it exactly when $C<1/(4\nu)$. Under the stated observation contract a randomized or history-dependent choice of intervals cannot improve on the best rate. Conditional on the last state and the chosen length, the expected interval return is $LJ(L)$. Its age-dependent increments decrease, and the unpaid advantage in an unfinished interval is bounded by the geometric sum. Dividing by total time gives the same upper bound.

Thus very rapid change can select *less* paid scrutiny when an observation expires too soon to earn its price. At $C=.75,\nu=.05$ the optimum is a check every seven rounds, giving net mean **.7655**. At $\nu=.4$ the same check technology cannot improve the mean .5 of never checking. For another comparison, at $C=.3,\nu=.1$ checking every three rounds earns **.8067**. Now let the incumbent see the realized output after acting. In this binary world it learns yesterday's true state for free. Acting on that state already earns .9; advance inspection is worth only .1 each round. The selected rule can keep *revising its ranking from experience* while discontinuing the paid checks. Counting formal reviews alone would misclassify its flexibility. Information value under changing environments and the distinction between observation channels are established themes. [Rivoire and Leibler](https://statbio.net/papers/Rivoire_2011.pdf).

Dekel, Ely and Yilankaya study the evolution of subjective preferences when matches reveal more or less about the other agent, including a broader class of mutants. Dewatripont and Tirole examine incentives to acquire and present information through advocacy. Stabilization by mutation in evolutionary games is established work. The present contribution joins paid, state-sensitive admission to strategic entry, finite access to a self-sustaining review practice, and a comparison with the inheritance of reporting standards. [Dekel, Ely and Yilankaya](https://cet.econ.northwestern.edu/dekel/pdf/evolution%20of-preferences.pdf), [Dewatripont and Tirole](https://doi.org/10.1086/250049), [Bauer, Broom and Alonso](https://arxiv.org/abs/1905.07839), [W6 commitment game](R6_strategic_values.md), [checker](../notebook/P4-R7-C001/advisers.py).
