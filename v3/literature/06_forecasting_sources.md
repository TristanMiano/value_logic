# P3-06 — forecasting sources and exact comparison

Contributor: **ChatGPT (GPT-6 Astra Pro)**, October 9, 2026 UTC.
Same-model internal, nonblind literature reconstruction. This is a selected
primary-source comparison, not a comprehensive priority survey or a contribution
gate decision. The corresponding
[review record](../work_logs/P3_06_2026-10-09_S1/reviews/literature_review.md)
states the retrieval and verification limits.

## 1. Result of the comparison

The common scalar construction in the preserved addendum is a finite-feature
adaptation of **Vovk's K29-star algorithm**. Its exact score and zero-allowance
potential are already in the literature. Appending decision features is also
an established defensive-forecasting technique. The finite rational allowance,
selected arithmetic-query adapter, issue-time prices, delayed records and
repricing contract must therefore be assessed as a specific adaptation and
integration. Calling the report a cost does not establish a new induction rule.

The restricted result remains useful: one actual scalar report can be scored
against the specified experts, continuous calibration tests and smooth decision
consumer without substituting the mean of separately calibrated random reports.
What has to be established locally is the exact finite implementation, error
certificate, feedback scope and connection to the project's versioned meanings.
Those obligations are addressed by the
[P3-06 derivation](../derivations/06_cost_forecast_refinement.md); source results
alone do not verify the code or the semantic adapter.

## 2. Inspected sources

These local identifiers supplement, without changing, the existing S01–S22
[source contracts](01_source_contracts.md). Locators below use the numbered
sections and printed pages of the identified document.

| ID | Primary source and inspected version | Exact comparison passages |
|---|---|---|
| F06-DF0 | Vovk, Takemura and Shafer, [Defensive Forecasting](https://www.probabilityandfinance.com/articles/08.pdf), Working Paper 8, revised January 22, 2005 | §3, Theorem 1 and following computability remark, printed pp. 3–4 |
| F06-DF | Vovk, [Non-asymptotic calibration and resolution](https://www.probabilityandfinance.com/articles/13.pdf), Working Paper 13, revised July 1, 2006; selected statements matched to [arXiv cs/0506004v4](https://arxiv.org/abs/cs/0506004v4) | §2, K29-star algorithm, Theorem 1, equations (1)–(4), printed pp. 2–3; §4 Theorem 2; §5 calibration discussion; Appendix A |
| F06-EXPERT | Vovk, [Defensive forecasting for optimal prediction with expert advice](https://arxiv.org/pdf/0708.1503), arXiv:0708.1503v1, August 10, 2007 | §2 Lemma 1; §3 quadratic-loss protocol, Lemma 2 and Theorem 1, printed pp. 4–5 |
| F06-AA | Vovk and Zhdanov, [Prediction With Expert Advice For The Brier Game](https://www.jmlr.org/papers/volume10/vovk09a/vovk09a.pdf), JMLR 10, 2445–2471, November 2009 | §2 Algorithm 1 and Theorem 1, printed pp. 2446–2447; §5 substitution function |
| F06-DEC | Vovk, [Competitive on-line learning with a convex loss function](https://www.probabilityandfinance.com/articles/14.pdf), Working Paper 14, revised September 2, 2005; [arXiv cs/0506041v3](https://arxiv.org/abs/cs/0506041v3) | §2 exposures and Theorem 1; §4 equation (15); §5 Theorem 2 and Remark 4; §6 “Mixing,” Corollary 4, printed pp. 16–17; §7 algorithm |
| F06-RECENT | Perdomo and Recht, [In Defense of Defensive Forecasting](https://arxiv.org/html/2506.11848v2), arXiv:2506.11848v2, October 24, 2025 | §4 Lemma 4.1 and root-approximation discussion; §5 equations (10)–(12), consumer-exposure features; §6 Lemma 6.1; §9.1 |
| F06-WEAK | Foster and Hart, [Smooth calibration, leaky forecasts, finite recall, and Nash dynamics](https://math.huji.ac.il/~hart/papers/calib-eq.pdf), author-hosted journal-format PDF, *Games and Economic Behavior* 109, 271–293, 2018 | §4 equation (19) and Theorem 10, printed p. 281; Appendix A, Lemmas 17–18, printed pp. 291–292 |
| S14, rechecked | Joulani, György and Szepesvári, [Online Learning under Delayed Feedback](https://proceedings.mlr.press/v28/joulani13.pdf), ICML/PMLR 28(3), 1453–1461, 2013 | §2/Figure 1; §3.1, Algorithm 1 BOLD, equation (1), Theorem 1 and its footnote 2 |
| S19, rechecked | Zhao, Kim, Sahoo, Ma and Ermon, [Calibrating Predictions to Decisions](https://proceedings.neurips.cc/paper_files/paper/2021/file/bbc92a647199b832ec90d7cf57074e9e-Paper.pdf), NeurIPS 2021 | §§2.1–2.2; §3.1 Definition 2/Proposition 1; §4.1 Definition 4; §4.2 Proposition 2; §§4.3–4.4 |
| F06-BRIA | Oesterheld, Demski and Conitzer, [A Theory of Bounded Inductive Rationality](https://arxiv.org/pdf/2307.05068), EPTCS 379, 421–440, 2023, [arXiv:2307.05068v1](https://arxiv.org/abs/2307.05068v1) | §2; §§4.1–4.4 Definitions 1–7; §5 Theorems 1–2; §6 Theorems 3–4; §8; Appendix A.2 construction |
| S01, retained | Garrabrant et al., [Logical Induction](https://intelligence.org/files/LogicalInduction.pdf), selected imports already audited in P3-01 | §§3.1–3.5; Theorems 4.3.3/4.3.6/4.3.8; exact scope remains governed by the [existing import audit](../work_logs/P3_01_2026-10-07_S1/reviews/li_desiderata_import_audit.md) |

## 3. Exact K29-star specialization

F06-DF's protocol permits arbitrary contexts before the report and binary
outcomes afterward. For a feature map continuous in the report, Theorem 1
bounds its cumulative residual norm by the forecast variance-weighted feature
norm. Its optional uniform feature bound supplies a square-root rate; the
finite-sum theorem itself does not require that bound. The source also names
bisection. F06-DF0 separately cautions that continuous computability alone is
not an exact sign/root oracle.

Here is our explicit identification. Put the current weight and supplied expert
reports in the context, and use the fixed finite mapping

```math
x_t=(w_t,q_{t,1},\ldots,q_{t,N}),\qquad
\Phi(p,x_t)=w_t\bigl(\alpha(q_{t,i}-p)_{i=1}^N,
                        \beta(b_j(p))_{j=0}^m\bigr).
```

Define $`K((p,x),(p',x'))=\langle\Phi(p,x),\Phi(p',x')\rangle`$.
The source score becomes exactly

```math
S_t(p)=\langle R_{t-1},\Phi(p,x_t)\rangle
       +\tfrac12(1-2p)\|\Phi(p,x_t)\|^2.
```

The continuation allows either favourable endpoint before searching for a
root. That tie/endpoint policy can differ from the source's stated choice;
the same sign inequality proves the same potential claim. It is not a claim
that all implementations return identical reports.

Two consequences are direct finite-coordinate calculations. The expert
coordinate becomes a squared-loss comparison after expanding the two squares;
the tent coordinates are the announced calibration residuals. The weights are
ordinary context coordinates. Neither weighting nor concatenating these
coordinates creates a new source theorem.

The locally recorded

```math
A_t=2\max\{0,(1-p_t)S_t(p_t),-p_tS_t(p_t)\}
```

is the exact maximum excess potential increment over the two possible outcomes.
Keeping this actual number gives a useful implementation contract when a
finite search stops. It is a direct algebraic adaptation, not evidence that
approximate defensive forecasting was previously absent. F06-RECENT §4 also
discusses approximate roots. Our score-specific Lipschitz account is needed
to distinguish input accuracy, residual accuracy and arithmetic work; a fixed
bisection count alone supplies none of the required asymptotic residual bound.

For $`W_T=\sum_t w_t`$, the sufficient conditions involving
$`\sum_t w_t^2/W_T^2`$ and $`\sum_t A_t/W_T^2`$ are conditions on our weighted
specialization. Known finite stakes may grow. The algebra remains meaningful
while its normalized bound can become uninformative. This distinction prevents
an arbitrary unbounded-value learning claim from being inferred from finite
weighted sums.

## 4. Ordinary expert aggregation is a stronger score-only comparator

F06-EXPERT §3 Theorem 1 guarantees, for unweighted binary squared loss,

```math
L_T\le L_{T,i}+\tfrac12\ln N
```

for every horizon and fixed expert. Advice may even depend continuously on the
current report. F06-RECENT §9.1 reconstructs this exponential-potential route.
This guarantee is stronger in horizon and library-size dependence than the
addendum's simple joint Euclidean bound.

Consequently an ordinary comparison must not be limited to a weak constant
predictor or an untuned generic mixture. Two comparisons serve different
purposes: the same-feature K29-star method checks whether the project's typed
integration changes information or numerical behavior; a strong squared-loss
aggregator tests the predictive tradeoff. The latter does not automatically
have the exact same tent/decision guarantees, and the former is permitted to
match every report. No empirical superiority is established by the present
source review.

F06-AA gives an explicit ordinary comparator. Its loss sums squares over all
outcome coordinates; for binary outcomes this is twice our scalar squared
loss. Algorithm 1 constructs generalized losses and uses a substitution
function. The binary specialization is $`p=(1+g_0-g_1)/2`$ when the generalized
losses $`g_y`$ use our scalar convention. Theorem 1's additive constant becomes
$`(\ln N)/2`$ after the same conversion. The development adapter uses a fixed
update rate $`2/w_{\max}`$ and current effective rate $`2w_t/w_{\max}`$ for
announced positive stakes bounded by $`w_{\max}`$. Its log/exp implementation
uses binary64, reports observed mixability slack, and does **not** certify the
ideal real-arithmetic guarantee from floating-point comparisons.

### 4.1 Comparator update: exponential potentials can serve simultaneous duties

**The current K29-star square-root expert rate is a feature/potential choice,
not an established unavoidable price of simultaneous calibration and actions.**
The score-only AA run does not exhaust the strongest credible ordinary
comparison. This update records a stronger mathematical comparator; it adds
no executable method, run, priority claim or contribution decision.

F06-EXPERT §2 Lemma 1 defends any forecast-continuous supermartingale. Section 3
Lemma 2 supplies the exponential squared-loss process; its proof gives the
Bernoulli Hoeffding exponential inequality, and Theorem 1 sums nonnegative
expert processes. The following simultaneous construction is a local consequence
of those ingredients, rather than a separately quoted theorem from the paper.

Consider immediate feedback, or one copy's settled subsequence. Announce a
finite expert/test/action family and a positive stake cap
$`0\le w_t\le w_{\max}`$, $`w_{\max}>0`$.
Choose an expert rate $`0<\eta\le2/w_{\max}`$ and fixed positive moment rates.
For regret $`R_{T,i}`$ to expert $`i`$, the process

```math
M^{\mathrm{exp}}_{T,i}=\exp(\eta R_{T,i})
```

uses the one-step source inequality at $`\kappa_t=\eta w_t\le2`$. For a
continuous bounded calibration test $`h_j`$, define

```math
E_{T,j}=\sum_{t\le T}w_th_j(p_t)(y_t-p_t),\qquad
V^{\mathrm{cal}}_{T,j}=\sum_{t\le T}(w_th_j(p_t))^2,
```

and use both signs of
$`\exp(\pm\lambda_jE_{T,j}-\lambda_j^2V^{\mathrm{cal}}_{T,j}/8)`$.
These are squared **one-step range** budgets, not the K29-star forecast-
variance term $`\sum p_t(1-p_t)\|\Phi_t\|^2`$.

For the smooth action mixture in §5, let $`A_{T,i}`$ be its realized weighted
regret to fixed action $`i`$, and put

```math
g_{t,i}=w_t(\bar C_t(p_t)-C_{t,i}(p_t)),\qquad
Z_{T,i}=A_{T,i}-\sum_{t\le T}g_{t,i}
       =\sum_{t\le T}w_t(\bar d_t(p_t)-d_{t,i})(y_t-p_t),
```

```math
V^{\mathrm{act}}_{T,i}=\sum_{t\le T}
          (w_t(\bar d_t(p_t)-d_{t,i}))^2.
```

The one-sided action process is
$`\exp(\lambda_iZ_{T,i}-\lambda_i^2V^{\mathrm{act}}_{T,i}/8)`$.
Centering by the known forecast gap is essential: uncentered smoothed action
regret need not have nonpositive forecast expectation. The smoothing guarantee
then bounds $`\sum_tg_{t,i}`$ by its already recorded slack.

Give each nonnegative process positive prior mass $`\pi_s`$, with masses
summing to one. Their sum is forecast-continuous when expert reports and the
specified consumer features are continuous in $`p`$. Applying Lemma 1 to that
sum gives one scalar forecast serving all the declared duties. Each component
is at most $`1/\pi_s`$, hence

```math
R_{T,i}\le\frac{\ln(1/\pi_i)}{\eta},\qquad
\pm E_{T,j}\le\frac{\ln(1/\pi_{j,\pm})}{\lambda_j}
                  +\frac{\lambda_jV^{\mathrm{cal}}_{T,j}}8,
```

with the analogous upper bound for $`Z_{T,i}`$ and the forecast gap added back
for action regret. A declared finite-horizon range bound permits prospective
rate tuning and square-root moment bounds while expert regret remains constant
in horizon for a fixed finite family. Retrospectively optimizing a rate for
which no process was run is not licensed. Restarting or mixing rates requires
its own accounting; delayed copies likewise sum their comparator costs.

This comparator involves exponential evaluation and a different defensive
potential. Its ideal existence result does not certify binary64 log/exp, the
current rational polynomial score, or its particular root-work budget.
Certified transcendental evaluation and an explicit potential-error allowance
would be needed for a corresponding finite numerical guarantee. The local
exact K29-star implementation remains a concrete restricted implementation;
its weaker expert rate is not evidence of a general joint-duty lower bound.

## 5. Decision features: a specific adaptation of an established bridge

F06-DEC defines an action's exposure as the difference between its losses on
the two outcomes. Equation (15) uses exposure residuals on both the chosen
decision and comparator to transfer forecast Bayes optimality into realized
regret. Corollary 4 explicitly combines feature maps. Its more general theorem
assumes a closed convex superdecision set, finite endpoint infima, bounded
RKHS evaluation and the stated tail conditions; its lexicographic report adds
a coordinate to handle Bayes ties. F06-RECENT §§4–6 give a closely related
consumer-moment formulation with continuous exposure.

The continuation's two-action block makes a narrower finite construction.
Write $`C_i(p)=b_i+d_i p`$, let $`\Delta(p)=C_1(p)-C_0(p)`$, and define

```math
s(p)=\mathrm{clip}\!\left(\tfrac12-\frac{\Delta(p)}{2\eta},0,1\right),
\qquad \eta>0.
```

The mixed action puts mass $`s(p)`$ on action 1. Its forecast loss is within
$`\eta/8`$ of the better pure action: on the nonconstant portion the excess
is $`|\Delta|/2-\Delta^2/(2\eta)`$, whose maximum is $`\eta/8`$.
If $`\bar d(p)=(1-s(p))d_0+s(p)d_1`$, append the two coordinates

```math
\Phi^{\mathrm{act}}_i(p,x_t)
 =w_t\gamma\bigl(\bar d_t(p)-d_{t,i}\bigr),\qquad i\in\{0,1\}.
```

Each is continuous for a positive smoothing width. Expanding actual-minus-
forecast losses gives, for each fixed action index,

```math
\sum_t w_t\bigl(\bar c_t(p_t,y_t)-c_{t,i}(y_t)\bigr)
 \le \sum_t w_t\eta_t/8+\frac{\sqrt{B_T}}{\gamma}.
```

This is our elementary exposure-difference specialization of the established
bridge, with explicit smoothing slack. Adding the expert and tent blocks
retains their coordinate guarantees for the same report, with the enlarged
feature norm included in $`B_T`$. The combination is scientifically worth
checking; feature concatenation by itself is not an originality claim.

The benchmark is a fixed action index across the announced loss contexts.
The bound controls **excess expected mixed-action loss**; it does not guarantee
the loss of a separately rounded or sampled action without another argument.
It is one-sided: its normalized upper bound can vanish while the signed regret
is negative and linear because changing actions beats every fixed action.
It is not an outcome-oracle bound. The earlier outcome-oracle bridge instead
requires small predictive error or a sufficiently accurate supplied expert.

Shrinking $`\eta_t`$ reduces forecast suboptimality but makes the features
steeper. Bounded slopes keep their magnitudes bounded, while the root-search
work can grow. That tradeoff belongs in the implemented allowance/resource
account. The result also presupposes the announced common-outcome loss table;
it does not construct counterfactual losses for agent-dependent alternatives.

## 6. Calibration of decisions has a declared consumer scope

S19 Definition 2 equates population-average predicted and actual loss for
specified loss and report-based decision-rule classes. Proposition 1 gives
optimality relative to those report-based rules. Direct feature-dependent
rules are excluded from that definition. Approximation normalizes by a loss
norm. Its sample guarantee retains an inner optimization problem; the practical
relaxation is not a free exact optimizer.

The two-action inequality above controls the *difference* between the mixed
action and each comparator. It need not separately calibrate the absolute
reported loss of each action. Common outcome-dependent costs cancel from
decision regret but remain in absolute loss-estimation error. Thus it is more
precise to call it a specified decision-regret bridge than unrestricted
decision calibration. Separate absolute exposure coordinates would support
separate loss-estimation claims under their own norms.

The fixed tents alone do not test arbitrary decision thresholds, stakeholder
weights or context selections. Adding an appropriate continuous consumer
feature is an explicit extension of the tested class, not a consequence of
ordinary marginal calibration. These distinctions preserve the existing S19
scope and avoid equating a weighted pathwise statement with a population
statistical guarantee.

### 6.1 Weak Lipschitz calibration has direct primary antecedents

F06-DF §5 Corollary 1, printed pp. 8–9, obtains vanishing time-normalized
residuals for every continuous test on a compact context/report space using a
universal RKHS. F06-WEAK §4 equation (19) and Theorem 10 treat a class of
Lipschitz tests valued in $`[0,1]`$ uniformly for each declared finite Lipschitz
constant. Its
Appendix A, Lemmas 17–18, constructs a Lipschitz partition of unity and a finite
uniform approximation basis. These are directly relevant antecedents for
extending finite continuous checking features; they establish no priority for
our selected grid or restart schedule.

Our one-dimensional tent specialization uses
$`f_m(p)=\sum_{j=0}^m f(j/m)h_{j,m}(p)`$. If $`\|f\|_\infty\le1`$ and
$`\mathrm{Lip}(f)\le L`$, interpolation gives
$`\|f-f_m\|_\infty\le L/m`$. Thus an epoch with weight $`W_e`$, grid size
$`m_e`$ and calibration residual vector $`E_e`$ has

```math
\sup_{\|f\|_\infty\le1,\ \mathrm{Lip}(f)\le L}
 \left|\sum_{t\in e}w_t(y_t-p_t)f(p_t)\right|
 \le \sqrt{m_e+1}\,\|E_e\|_2+\frac{LW_e}{m_e}.
```

Growing grids and epoch restarts therefore require explicit control of both
summed terms, unfinished-epoch prefixes, and any pending feedback. Merely
increasing the number of tents proves no convergence. The quantifier is uniform
over each class with a **fixed** bound on the Lipschitz constant, not uniform
over unrestricted constants or discontinuous indicators.

Neither inspected source is claimed to contain our exact epoch schedule.
Foster–Hart's finite forecast grid is also a different object from a tent-feature
grid. Their introductory restart remark concerns recall and is not used as a
source for an accuracy schedule. The current implementation has fixed settings
and a maximum of 64 bins; its four-bin development run does not execute a
growing-grid asymptotic construction. Weighted/delayed resource conditions and
any proposed expanding implementation need their own argument.

## 7. Delayed copies inherit a construction, with a local pathwise proof

S14's BOLD algorithm uses an available copy whose preceding feedback has
arrived, creating another only when all copies are busy. Its number of copies
is one plus the maximal outstanding-feedback count. Theorem 1 assumes a
nondecreasing concave base-regret bound with value zero at zero, and delays
independent of the forecaster's current prediction, to give its stated expected
regret transfer. Those hypotheses must accompany an import of that theorem.

P3-06 uses the same scheduling idea. Its stronger-for-this-fragment pathwise
algebra needs no stochastic independence theorem: each copy has a residual
certificate for its settled subsequence, and

```math
\left\|\sum_{k=1}^{K}R^{(k)}\right\|^2
 \le K\sum_{k=1}^{K}\|R^{(k)}\|^2
 \le K\sum_{k=1}^{K}B^{(k)}.
```

This elementary recombination is valid because the binary potential bound
holds for every outcome after each report. It does not warrant dropping
independence from S14's more general expected-regret theorem. It also does not
make growing concurrency free or assert that the settled population represents
the unresolved population. A paid proof policy must still establish useful
coverage, copy counts and costs. P3-07 owns that policy question.

## 8. BRIA is a different, already value-directed inductive criterion

F06-BRIA §2 uses finite option sets, realized rewards in $`[0,1]`$, and current-
round decision quality; rewards of unchosen alternatives are not supplied.
A hypothesis recommends an option and promises a reward. Definitions 2 and 6–7
combine

```math
\limsup_{T\to\infty}\frac1T\sum_{t\le T}(\alpha_t^e-r_t)\le0
```

with coverage: if $`B_h=\{t:h_t^e>\alpha_t^e\}`$ is infinite, some test set
$`M_h\subseteq\{t:\alpha_t^c=h_t^c\}`$ must satisfy

```math
\sum_{t\in M_h,\ t\le T}(r_t-h_t^e)\longrightarrow-\infty
\quad\hbox{as }T\to\infty\hbox{ through }B_h.
```

**Quantifier clarification.** Definition 4 does not require
$`M_h\subseteq B_h`$. The outpromise set indexes the horizons at which the
record must diverge in Definition 6; tests need only match the recommended
action. Definition 4 also permits finite test sets, although they cannot provide
the required divergence when $`B_h`$ is infinite. The
[sparse recurring-error witness](../work_logs/P3_06_2026-10-09_S1/reviews/bria_sparse_coverage_witness.md)
has vanishing time-normalized forecast regret and vanishing normalized residuals for bounded report tests,
eventually zero fixed-action regret, and no reward overestimation, yet every
permitted test set has record zero for an infinitely outpromising hypothesis.
Its failure is not absence of infinite test sets. This is a criterion
non-implication, not a trace of our algorithms; the stronger constant expert
regret comparator with a perfect supplied expert excludes this particular tape.

Theorem 1 gives existence for a computably enumerable class of
$`O(g(t))`$-computable hypotheses, with $`g\in\Omega(\log)`$, using
$`O(g(t)q(t))`$ time for suitable arbitrarily slowly diverging computable
$`q`$. Theorem 2 gives its qualified same-complexity obstruction. Theorems 3–4
derive average-reward lower bounds from efficiently available guarantees or
class-relative algorithmic randomness. These are source-stated results, not
imports into P3-06.

**Comparison.** Our finite experts forecast a shared outcome. Once its label
arrives, all their squared losses can be computed. BRIA hypotheses have an
action-and-promise type, and testing concerns actually taking the recommended
action. A low squared-loss regret bound therefore supplies neither its test sets
nor the divergent rejection records. Likewise our resolved-copy certificate
does not force the learner to obtain feedback on an attractive untested
possibility.

BRIA's reward estimates need not satisfy a two-sided calibration condition.
For example, with one option paying 1 forever, an agent estimating 0 satisfies
the BRIA criterion relative to the singleton hypothesis that recommends that
option and also promises 0. There is no overestimation and no outpromising
hypothesis. Those same numbers interpreted as binary forecasts are wholly
miscalibrated. This is a small definition-level witness for a restricted
hypothesis class, not a counterexample to BRIA's richer-class theorems.

Conversely, a finite forecast library leaves efficiently describable missing
strategies outside its comparison set. Merely relabelling its output as value
does not close that gap. A future BRIA reduction would need an explicit
action/promise encoding, tested hypothesis class, feedback schedule and proof
of both criterion clauses. An affine conversion of uniformly bounded costs is
different from an arbitrary changing or unbounded stake stream.

BRIA is therefore a substantial nearby antecedent for a value-directed,
computationally bounded inductive architecture. It is not a theorem that our
present scalar implementation meets that architecture's guarantees, nor is
P3-06 a generalization of BRIA. Finite regret and BRIA coverage address distinct
questions. No maximally efficient paid reasoning policy follows from either.

## 9. Exact relationship to the retained LI duties

The P3-01 LI import audit is retained rather than redone. Its recurring
calibration result is a limit-point statement; its selected convergence result
has additional deferral and timely-feedback assumptions. Those remain separate
from the finite continuous-test theorem here. The full efficient-trader
criterion quantifies over a much richer computable comparison mechanism than
our announced finite expert and feature lists.

| Duty | What this construction can establish in its own fragment | What this comparison does not establish |
|---|---|---|
| U06 | Competition on a recurring, computably supplied query family before individual answers arrive | Discovery of a missing arithmetic identity or efficient universal pattern coverage |
| U07 | Actual scalar-report residuals for the announced continuous tests | Every calibration selection, every context, or LI's unrestricted criterion |
| U08 | Issue-weighted regret against the same fixed supplied expert indices | Every efficient trader, dynamic oracle or optimal score-only rate |
| U09 | Explicit settled-copy certificates with the copy factor charged | Coverage of missing labels or a useful acquisition policy |
| V03 | The declared smooth fixed-action bridge; separately, the conditional outcome-oracle bridge | Counterfactual identification, absolute loss calibration without its features, or paid policy optimality |

The possible project delta is the exact integrated service: which scoped
mathematical outcomes and cost queries it supports, what records permit later
rescoring, and what guarantee survives finite arithmetic and delayed evidence.
Its magnitude and contribution status require the integration evidence and
the author's later gate decision. This review establishes the closest inspected
antecedents and the claims they prevent us from overstating.
