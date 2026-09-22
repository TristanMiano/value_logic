# F01 continuation — Reconstruction and information contracts

Research date: September 21, 2026 (America/Los_Angeles).
Source: `450048c1b243a33fa8d5a07b59ecf2ff5bb5d76c`.
Status: example-level derivation and same-agent audit, not a selected calculus.

This supplements the [principal F01 note](01_requirements_and_separating_examples.md).
The eight original examples remain the common test cases. The purpose here is
not to add enough structure to make a favorite representation win. It is to
check exactly what each operational question needs, find positive restricted
repairs, and distinguish exact numerical recovery from a useful approximate
conclusion. The arguments are conditional on the finite tables and explicitly stated
real-valued or countable extensions below. None is claimed as a new theorem about the eventual calculus.

This is a same-agent, non-blinded reconstruction and alternative-derivation
pass. It is not independent external review and does not discharge F16.
The [session record](../work_logs/F01_2026-09-21_S2.md) records scope and timing.

## A. Reconstruction of the original questions

### A.1 Cost, tolerance, and task scope: E01–E02

In E01, the reference minus the cheap prediction is exactly $z^3$. On either
of the two inputs $z=\pm a$, its absolute value is $a^3$. The cost difference
is seven work units, so the cheap-minus-accurate combined loss is
$a^3-7\lambda$. This separately establishes the preference boundary
$a^3\leq7\lambda$; it does not establish error admissibility $a^3\leq\epsilon$
or budget feasibility. At $a=1/2$ and $\lambda=1/56$, the scores are

$$
\frac18+\frac1{56}=\frac17,
\qquad 8\frac1{56}=\frac17.
$$

Only the accurate model meets $\epsilon=1/100$. The collision concerns the
combined number alone: retaining the model identity together with a table of
its risks would supply additional information and evade that restriction.
A scalar can also answer feasibility alone, for example the minimum of two
properly normalized admissibility margins. Failure of this particular combined
score is not a general prohibition on scalar representations.

In E02, the loss difference is $4(1-\theta)-1=3-4\theta$. The zero occurs at
$3/4$ and the sign reverses across it. A useful refinement concerns a restricted
task family. For arbitrary two-coordinate errors $u,v$, define

$$
d(\theta)=\theta(u_1-v_1)+(1-\theta)(u_2-v_2).
$$

If only $\theta\in[\ell,r]$ is admitted, where $0\leq\ell\leq r\leq1$, then

$$
d(\theta)\leq0\text{ for all admitted }\theta
\quad\Longleftrightarrow\quad d(\ell)\leq0\text{ and }d(r)\leq0.
$$

For $\ell<r$, each intermediate value is a convex combination of the endpoint
values; the singleton case is immediate. Thus global coordinatewise dominance
can be stronger than the actual task question requires. On $[1/4,3/4]$, E02's
$B=(1,1)$ is no worse than $A=(0,4)$ everywhere, although the two are incomparable
when all weights in $[0,1]$ are admitted.

**Operational consequence.** A numerical encoding, using ordinary numeric
order as the comparison, is not the same thing as a numerical code plus a
context-sensitive decoder. In particular, no ordinary real-number order can
reflect a partial order containing incomparable elements in both directions:
real numbers always satisfy at least one of $a\leq b$ or $b\leq a$. This does
not exclude coding a partially ordered object into a real and using a different
decoder. F02 must state which meaning of “scalar representation” it is testing.

### A.2 Joint dependence: E03

The two scenarios give component means one in both alignments. Their minimum
is either constantly $-1$ or distributed equally over $-1,3$. Reconstructing
from the four possible joint cells gives $4t-1$ with
$t=\Pr(X=3,Y=3)\in[0,1/2]$. Hence the exact-score collision and sharp interval
$[-1,1]$ are both correct, but use different information contracts.

The three-by-three covariance counterexample also survives direct summation.
Each row and column has six counts out of eighteen. The signed corner sum
for $XY$ is zero in each table. The minimum receives negative contributions
from the first row and first column and a positive contribution at $(1,1)$,
yielding $-7/18$ and $-9/18$. Covariance therefore does not generally substitute
for the needed nonlinear joint information. Section B identifies an important
restricted case where it does suffice.

### A.3 Sequential use: E04

Subtracting the ideal composite directly gives $100(1/100)+1/50=51/50$.
Adding and subtracting $g(\hat f(z))$ separates downstream approximation error
at the *actual* input from propagation of upstream error. This rederives
$\eta+K\delta$, including its attained equality case.

The reachable-input condition is indispensable. When $f=0$, $\hat f=\delta$,
$g=0$, and $\hat g(u)=Mu/\delta$, exactness at the sole ideal input does not
control the actual input: the composite error is $M$. No first-stage accuracy
claim repairs that missing downstream scope by itself.

Scope also includes weighting, not just the name of a domain. For a uniform
finite population of $n$ cases, an error of one on one case and zero elsewhere
has average $1/n$. Restriction to the bad case has average one. More generally,
for nonnegative loss and a positive-probability event $A$,

$$
\mathbb E[L\mid A]
=\frac{\mathbb E[L\mathbf1_A]}{\Pr(A)}
\leq\frac{\mathbb E L}{\Pr(A)}.
$$

A global average can therefore give a weakened subdomain bound, not generally
the original bound. This is a finite illustration of the already available
[phase-one transport results](../../formalism/08a_transport_routing.md), not a
new universal rule. The later calculus may admit other error aggregations.

### A.4 Evidence and interpretations: E05–E06

For E05, nonemptiness and a lower bound answer different parts of the question.
Both universal sign claims over the empty set are mathematically true; neither
satisfies the explicitly requested nonempty basis. Refinement preserves a
universal guarantee only when it restricts the same quantity under unchanged
interpretation. A changed task, a changed unit, or a retracted premise is not
such a refinement merely because some displayed numbers become smaller.

For E06, an adapter sees a fiber of the residue map, not the original input.
For parity inferred from a mod-three residue, each fiber has two equiprobable
inputs with opposite parity. For mod-three inferred from parity, each fiber
contains three equiprobable target residues. A deterministic adapter can choose
only one answer on each fiber. A randomized adapter averages those conditional
success rates and cannot exceed their maximum. This reconstructs losses $1/2$
and $2/3$ without relying on exhaustive search. The paired residues are injective
on the six-element population because a difference divisible by both two and
three is divisible by six.

**Interpretation clarification.** The finite addition tables give interpreted
algebraic specifications. The distinctness of named elements is part of the
stipulated finite interpretation, not something to derive from positive
equations alone: a one-element algebra satisfies any collection of equations.
Similarly, the external decoder losses concern the specified residue interface,
not a general ranking of proof systems. Both restrictions should survive reuse
of this example.

### A.5 Recoding and attainable policies: E07–E08

The inverse of $h(x)=x/(1+|x|)$ is $y/(1-|y|)$ on $(-1,1)$. On the nonnegative
branch, substituting this inverse in transported addition gives
$(a+b-2ab)/(1-ab)$. Because $a,b<1$, the denominator is positive. The transported
operation is exact; retaining ordinary addition after squashing is not. Section
E sharpens both the scaling and precision claims.

For the countable example, summation by shifting the geometric series gives
$\sum_{k\geq1}k2^{-k}=2$. The original finite identity and geometric remainder
provide a separate check. The tail starting at eight is
$2^{-8}/(1-1/2)=1/128$. The range of an object, the finiteness of its expectation,
and the range of its encoding remain distinct.

For E08, the four deterministic signal policies have values
$1,1,4p-1,3-4p$. Any admissible randomized policy is a mixture of deterministic
ones; its randomization supplies no additional information about the hidden
scenario beyond the observed signal. For $p\geq1/2$, following is optimal before
cost. Optional acquisition therefore has value $\max\{1,4p-1-\kappa\}$.
Section G makes the quantifier and attainability conditions explicit.

## B. When covariance is enough, or still useful

### B.1 Exact reconstruction on known binary supports

This is a positive boundary on E03's negative result, not an assumption that
future value objects must be binary or probabilistic.

Let $X\in\{a,b\}$ and $Y\in\{c,d\}$, with $a<b$, $c<d$, and supplied marginal
probabilities $\alpha=\Pr(X=b)$, $\beta=\Pr(Y=d)$. Write
$X=a+(b-a)B$ and $Y=c+(d-c)C$ for binary indicators. If
$t=\Pr(B=1,C=1)$, their joint table is forced to be

$$
\begin{array}{c|cc}
 & C=0 & C=1\\
B=0&1-\alpha-\beta+t&\beta-t\\
B=1&\alpha-t&t
\end{array}
$$

and is a probability table exactly when

$$
\max(0,\alpha+\beta-1)\leq t\leq\min(\alpha,\beta).
$$

The covariance simplifies to

$$
\mathrm{Cov}(X,Y)=(b-a)(d-c)(t-\alpha\beta).
$$

Consequently known binary supports, both marginal laws, and covariance determine

$$
t=\alpha\beta+
\frac{\mathrm{Cov}(X,Y)}{(b-a)(d-c)},
$$

and therefore every finite joint payoff query, including the expected minimum.
For E03's supports $\{-1,3\}$ and half marginals, covariance $-4$ yields $t=0$
and covariance $4$ yields $t=1/2$, exactly distinguishing the two alignments.
The original three-valued counterexample does not contradict this binary result.

An alleged covariance can also be incompatible with the marginals. For binary
$0,1$ variables with half marginals, covariance one would require $t=5/4$,
outside $[0,1/2]$. That is inconsistent supplied information, not merely an
unidentified joint law. A zero-width but invalid summary is not a certificate.

**Requirement refined.** Sufficiency depends on the admitted support and query
family, and compatibility of supplied statistics must be checked. “Keep the
covariance” is neither always adequate nor always useless.

### B.2 Sharp bounds when covariance does not identify the answer

There is a stronger positive result for the *same* three-valued setting as the
original covariance counterexample. Let both marginals be uniform on
$\{-1,0,1\}$. With no covariance supplied, the sharp interval for
$\mathbb E\min(X,Y)$ is $[-2/3,0]$. The upper bound follows from
$\min(X,Y)\leq X$ and $\mathbb EX=0$, and is attained by $Y=X$. The lower
bound follows pointwise from

$$
\min(X,Y)\geq-\mathbf1_{X=-1}-\mathbf1_{Y=-1},
$$

and is attained by $Y=-X$. Convex mixtures of these joint laws retain the
marginals and fill the whole interval.

Now also supply covariance zero. The mean of the minimum is still not uniquely
determined, but its **sharp interval is $[-1/2,-1/3]$**. Here is a complete
finite-dimensional derivation. Transposing a joint table does not change the
marginals, cross-moment, or symmetric minimum query. Averaging a table with
its transpose therefore lets us compute the range using symmetric tables
without excluding any attainable target value. Write such a table as

$$
P=\begin{pmatrix}a&b&c\\b&d&e\\c&e&f\end{pmatrix}.
$$

All rows sum to $1/3$. Because both means are zero, covariance zero is
$a+f-2c=0$. Eliminating $a,d,f$ using the row sums gives

$$
b+e+4c=\frac23,
\qquad d=4c-\frac13.
$$

Nonnegativity of $d,b,e$ forces $1/12\leq c\leq1/6$. Direct evaluation of the
minimum table yields

$$
\mathbb E\min(X,Y)=-b-e-2c=-\frac23+2c,
$$

hence the claimed interval. To show that no hidden constraint narrows it, use
for every $c\in[1/12,1/6]$ the table

$$
P_c=\begin{pmatrix}
c&1/3-2c&c\\
1/3-2c&4c-1/3&1/3-2c\\
c&1/3-2c&c
\end{pmatrix}.
$$

Every entry is nonnegative, every row and column sums to $1/3$, covariance is
zero, and the displayed target formula holds. This constructs every point of
the interval. Its two endpoints have tables

$$
P_{\mathrm{low}}=\frac1{12}
\begin{pmatrix}1&2&1\\2&0&2\\1&2&1\end{pmatrix},
\qquad
P_{\mathrm{high}}=\frac16
\begin{pmatrix}1&0&1\\0&2&0\\1&0&1\end{pmatrix}.
$$

Independence would instead select the single value $-4/9$ from the uniform
nine-cell table. Covariance zero alone does not justify that choice.

This matters operationally. The question whether the expected bottleneck is
at least $-3/5$ is not uniformly settled by the marginal laws: the
countermonotone case reaches $-2/3<-3/5$. Adding covariance zero does certify
it, because every remaining joint law has value at least $-1/2>-3/5$.
Exact reconstruction remains impossible, yet the additional statistic makes a
useful tolerance-relative inference possible. A summary should not be judged
useless solely because it fails an exact-recovery test.

### B.3 An alternative derivation weakens the required information

The same sharp interval can be certified from less than the full marginal
laws. Fix dimensionless coordinates on the declared payoff scale. For any
$x,y\in[-1,1]$, the following pointwise inequalities hold:

$$
\frac{x+y+xy-1}{2}
\leq\min(x,y)
\leq\frac{x+y}{2}-\frac{(x-y)^2}{4}.
$$

For the lower inequality, suppose $x\geq y$. Then
$1-xy-|x-y|=(1-x)(1+y)\geq0$; the other order is symmetric.
Substitute $\min(x,y)=(x+y-|x-y|)/2$. For the upper inequality use
$|x-y|\leq2$, so $(x-y)^2\leq2|x-y|$, and substitute the same identity.

Consequently the hypotheses

$$
|X|,|Y|\leq1,
\quad \mathbb EX=\mathbb EY=0,
\quad \mathbb EX^2=\mathbb EY^2=2/3,
\quad \mathbb E[XY]=0
$$

already imply

$$
-1/2\leq\mathbb E\min(X,Y)\leq-1/3.
$$

These are support and moment conditions, not complete marginal distributions.
The endpoint tables in B.2 satisfy them, so the bounds are sharp even on this
larger admitted class. Their mixtures fill the interval as before. This is a
second proof route, not an independent reviewer: it was derived in the same
research session.

The full-data and reduced-data arguments thus agree, while exposing different
information costs. No claim is made that these two inequalities are optimal for
every other possible collection of moments. For instance, zero second moments
would additionally force both variables to be zero, a fact these two bounds
alone do not exploit. The later calculus must earn any claimed completeness
beyond the specific fragment actually analyzed.

The bounded-support premise is essential even after the other hypotheses have
been weakened to moments. For any $a>0$ with $a^2\geq4/3$, put probability
$1/(3a^2)$ on each of $(a,0),(-a,0),(0,a),(0,-a)$, and put the remaining
$1-4/(3a^2)$ at $(0,0)$. These probabilities are nonnegative and sum to one.
Both means are zero, both second moments are $2/3$, and the cross-moment is
zero. But the expected minimum is $-2/(3a)$: only the two negative-axis points
contribute. At $a=6/5$ this is $-5/9<-1/2$; at $a=4$ it is
$-1/6>-1/3$. Thus neither endpoint guarantee follows from those moments alone.
The positive rule uses the support bound, not merely the same numerical
variances. The rational five-point countermodels make that dependency explicit.

A weaker positive bound survives without the support condition. Set $D=X-Y$.
The same moment premises give $\mathbb ED^2=4/3$. If
$m=\mathbb E|D|$, averaging $(|D|-m)^2\geq0$ gives $m^2\leq4/3$.
Also $m>0$, since the second moment is positive. Therefore the mean of the
minimum lies in $[-1/\sqrt3,0)$. The five-point family above, now allowing
$a\geq2/\sqrt3$, attains every point of this interval: its value is
$-2/(3a)$, the lower endpoint occurs at $a=2/\sqrt3$, and values approach but
never reach zero as $a$ increases. Losing the support premise changes the
available guarantee; it does not erase all useful conclusions from the moments.
This interval claim uses ordinary real values and finite probability tables,
not an infinite-support distribution with undefined moments.

### B.4 No uniform strict margin is not the same as an ambiguous sign

The last interval also exposes an endpoint distinction relevant to E05.
Every admitted expected minimum is strictly negative, but no fixed negative
margin works for the whole class. Keeping only its closed hull would add zero
as a possible endpoint and lose that distinction. The elementary scalar
version is $S=\{-1/n:n\geq1\}$ versus $S\cup\{0\}$: both have infimum $-1$
and supremum zero, while “every admitted value is negative” holds only for the
first. The formulas $-1/n<0$ and $-1/n\to0$ prove the assertion; checking a
large finite prefix would not establish the missing-attainment claim.

A closed interval remains a valid conservative bound. It need not be a complete
representation for a *strict-sign* query on an infinite model class. A candidate
can retain endpoint-attainment information, use a richer range, or restrict its
fragment to sets where the relevant extremum is attained. If the consumer asks
only for a non-strict bound, that additional distinction may be unnecessary.
Nothing here refutes the finite-set statements or changes the phase-one rules.

## C. Nested operations can expose any missing interaction order

The original triple example extends to a small explicit family. Fix $n\geq2$.
Let $P_0$ be uniform on binary strings $b\in\{0,1\}^n$ with even parity, and
$P_1$ uniform on strings with odd parity. Each support has $2^{n-1}$ strings.

Choose any proper subset $I$ of $k<n$ coordinates and any assignment to it.
There are $n-k$ unassigned bits. Choose all but one freely; the last is uniquely
fixed by the required parity. Thus each assignment has $2^{n-k-1}$ completions
in either model and probability

$$
\frac{2^{n-k-1}}{2^{n-1}}=2^{-k}.
$$

Every proper-subset marginal law is consequently identical in the two models.
Nevertheless $\min_i B_i$ is one only on the all-ones string. That string has
one definite parity, so its mean is $2^{1-n}$ in that parity model and zero in
the other. This proves the distinction for every $n$, not only the tested cases.

For payoffs $Z_i=M B_i$ with $M\geq0$, the minimum-mean difference is $M2^{1-n}$. Setting
$M=2^{n-1}$ keeps the difference exactly one while leaving all proper-subset
marginals matched. Thus a fixed integer bound $r\geq1$ on retained joint interaction order
cannot answer all nested minima exactly: use $n=r+1$. Over an unbounded payoff
family it also cannot guarantee an arbitrarily specified finite absolute error
from those marginals alone: choose $M$ so that $M2^{1-n}>2\epsilon$.
One common reported number cannot be within $\epsilon$ of both target values.

There are two important limits on that statement. The negative result targets
summaries restricted to these marginal laws, not arbitrary scalar codes or
operation-specific information. Also, with $M$ fixed, this particular parity
gap decreases with $n$. That observation is not a proof that all missing
higher-order information is negligible for a bounded model class.

**Requirement refined.** An advertised composition-depth or approximation
contract needs its own evidence. A positive binary example cannot silently
become a closure claim for unrestricted nesting. The original triple fixture
is retained as the smallest nontrivial pairwise-law witness.

## D. Shared uncertainty can preserve a comparison that intervals discard

This is a nonprobabilistic counterpart of E03 and a refinement of E05. Suppose
the same unknown $z\in\{0,K\}$ affects candidate and fallback losses:

$$
C(z)=z+1,\qquad F(z)=z+3,\qquad K>2.
$$

All losses are nonnegative. Using the candidate improves on the fallback by
$F(z)-C(z)=2$ for every admitted $z$. Separate loss ranges, however, give only

$$
C\in[1,K+1],\qquad F\in[3,K+3],\qquad
F-C\in[2-K,K+2].
$$

The separate interval calculation is a sound outer bound; it has not proved a
negative improvement. It has lost a known positive guarantee by forgetting the
shared dependence. At $K=100$, the exact improvement is two while the outer
interval is $[-98,102]$.

The information-loss witness is exact. Replacing the joint pairs

$$
\{(1,3),(K+1,K+3)\}
\quad\text{by}\quad
\{(1,K+3),(K+1,3)\}
$$

preserves both marginal loss ranges but changes the minimum improvement from
two to $2-K$. Ranges alone cannot distinguish the two questions. Keeping the
shared relation $F-C=2$ suffices for the first comparison; keeping the entire
underlying uncertainty source is unnecessary for this one query.

There is an exact finite criterion for when the interval lower bound is sharp.
For a nonempty finite joint set $S$ of pairs $(c,f)$, write
$c_{\max}=\max_S c$, $f_{\min}=\min_S f$. Then

$$
\min_{(c,f)\in S}(f-c)\geq f_{\min}-c_{\max},
$$

with equality exactly when one admitted pair simultaneously satisfies
$f=f_{\min}$ and $c=c_{\max}$. To prove this, subtract the right side:

$$
(f-c)-(f_{\min}-c_{\max})
=(f-f_{\min})+(c_{\max}-c).
$$

Both terms are nonnegative, and their sum is zero exactly when both vanish.
Finiteness ensures a minimizing pair exists. A rectangular product of the
marginal sets contains such a pair, but taking that product enlarges the
original joint uncertainty unless all combinations were already admitted.

The finite-attainment hypothesis matters to the equality characterization.
For the infinite set $S=\{(1-1/n,1/n):n\geq1\}$, the infimum comparison equals
$-1=\inf f-\sup c$, yet no pair attains either endpoint. Replacing finite
minima/maxima by infima/suprema would therefore require a different statement
about approaching the endpoints, not the unchanged co-attainment condition.

**Requirement refined.** Reusing a common uncertainty variable and introducing
an independently varying copy are different operations. Conversely, a
conservative bound need not be an error in reasoning; its information loss and
possible decision cost should be visible. No diagnosis of the phase-one
experiment's causes is inferred from this constructed example.

## E. Which transformations preserve the requested arithmetic?

### E.1 Ordinary sum comparisons impose more than monotonicity

Work in the usual ordered real field for this diagnostic. Suppose a recoding
$h:\mathbb R\to\mathbb R$ preserves every weak comparison of two-component
additive totals:

$$
x_1+x_2\leq y_1+y_2
\quad\Longleftrightarrow\quad
h(x_1)+h(x_2)\leq h(y_1)+h(y_2).
$$

This includes preserving ties. Comparing $(x,0)$ with $(y,0)$ shows that $h$
is strictly increasing. Comparing the equal totals $(x,y)$ and $(x+y,0)$ gives

$$
h(x)+h(y)=h(x+y)+h(0).
$$

Set $g(x)=h(x)-h(0)$. Then $g$ is additive and strictly increasing. Additivity
implies $g(m/n)=(m/n)g(1)$ for rational $m/n$: first use integer sums and signs,
then $n g(m/n)=g(m)$. For real $x$, squeeze it between rational sequences
$r_j\uparrow x$ and $s_j\downarrow x$. Monotonicity gives

$$
r_jg(1)\leq g(x)\leq s_jg(1),
$$

so $g(x)=xg(1)$. Consequently

$$
h(x)=a x+b,\qquad a>0.
$$

Conversely, this form preserves all fixed-length additive comparisons because
both totals acquire the same offset. Thus positive affine recodings are exactly
the recodings satisfying the displayed *ordinary two-component sum* contract.
No bounded strictly monotone recoding on all real inputs can meet that contract.
This does not contradict exact bounded encodings with transported operations.

If different component counts are compared without any correction, the offset
also matters. The tied plans $(0)$ and $(0,0)$ force $h(0)=2h(0)$, hence $b=0$.
For example, $h(x)=2x+3$ preserves every equal-length sum ordering, but sends
plans $(2)$ and $(1,0)$, with original totals two and one, to totals seven and
eight. Positive linear scaling preserves all finite-length comparisons; a
nonzero affine offset requires retaining and correcting component count.

These are conditional requirements of the admitted operation, not a derivation
of a unique value scale from fallibilism. A consumer asking only for one good
action can require less than preservation of every weak numerical ordering;
section F makes that distinction explicit.

### E.2 A bounded code needs an appropriate precision contract

For nonnegative $x,y$, E07's recoding satisfies the exact identity

$$
|h(x)-h(y)|=\frac{|x-y|}{(1+x)(1+y)}.
$$

Therefore, on a declared range $0\leq x,y\leq M$,

$$
\frac{|x-y|}{(1+M)^2}\leq|h(x)-h(y)|\leq|x-y|.
$$

An encoded error at most $\eta$ then implies a decoded discrepancy at most
$(1+M)^2\eta$, provided both decoded values lie in the declared range. An
estimated code can first be projected onto $[0,h(M)]$, which cannot increase its
error relative to a true code in that interval. Without that range condition,
$M=1$, true code $1/2$, and reported code $3/5$ give decoded error $1/2$, exceeding
$4(1/10)$. This is a constructive finite-range repair, not an unconditional
inverse-Lipschitz claim. Without an upper
range bound, no finite global constant in this inverse-error estimate exists:
use adjacent values $n,n+1$ and let $n$ increase.

There is also an exact interval calculation. Suppose the observed code is $z$
with radius $\eta$, and $0\leq z-\eta\leq z+\eta<1$. The decoded compatible
interval is

$$
\left[\frac{z-\eta}{1-z+\eta},\frac{z+\eta}{1-z-\eta}\right],
$$

whose width, after bringing the two fractions to a common denominator, is

$$
\frac{2\eta}{(1-z)^2-\eta^2}.
$$

As the upper encoded endpoint approaches one, a fixed encoded tolerance can
correspond to a very large decoded interval. If a nonempty compatible encoded
interval reaches arbitrarily close to one, its decoded upper range is unbounded.
An alleged exact code of one, by contrast, is outside the exact image and is
not itself a valid representation of a finite real number.

The operational consequence can concern decisions, not just reconstruction.
Give two named actions the unknown scores $(n+d,n)$ or $(n,n+d)$, where $d>0$.
Suppose only the individually approximate codes are visible. In both models,
both reported codes may equal the common midpoint of $h(n)$ and $h(n+d)$ once

$$
h(n+d)-h(n)=\frac{d}{(n+1)(n+d+1)}\leq2\eta.
$$

For any fixed $d,\eta>0$, a sufficiently large $n$ meets that inequality. One
cannot then distinguish the optimal action from those reports. A deterministic
choice has regret $d$ in one model; a randomized choice has worst-model expected
regret at least $d/2$. Taking $d$ arbitrarily large shows why a fixed absolute
code-error bound alone supplies no fixed global real-unit regret guarantee.
This assumes no additional score, order, or correlated-error information. A
known shared additive error, for example, would be a different contract.

**Requirement refined.** Exact information preservation, operation preservation,
and error/decision preservation are separate questions. The bounded code is not
rejected; its operations, working range, precision, and claimed tolerance must
be specified together. Fixed-width absolute precision is not the only allowed
representation scheme.

## F. Exact values can be unnecessary for the actual decision

### F.1 Best possible numerical accuracy from a specified summary

For this finite diagnostic, let $Z$ be a set of permitted inputs, $s(z)$ a
proposed summary, and $\psi(z)\in\mathbb R$ the numerical answer requested. At a
particular observed summary $c$, let the nonempty compatible fiber be
$Z_c=\{z:s(z)=c\}$. Suppose its answer set has finite minimum $m$ and maximum $M$.
Every number $a$ reported from that summary alone has worst-case absolute error

$$
\sup_{z\in Z_c}|\psi(z)-a|\geq\max\{M-a,a-m\}\geq\frac{M-m}{2}.
$$

The midpoint $a=(m+M)/2$ attains this bound, because every possible answer lies
in $[m,M]$. Thus an $\epsilon$-accurate numerical decoder exists on this fiber
exactly when $M-m\leq2\epsilon$. For a nonempty bounded but infinite answer set,
the same proof uses infimum and supremum. An empty fiber is incompatible
information, not a zero-error reconstruction. An unbounded answer set permits
no finite uniform absolute-error estimate.

For E03's fully known two-point marginals, the sharp answer range is $[-1,1]$:
zero is a minimax numerical estimate with error one, even though exact recovery
is impossible. An error-one estimate does not certify the sign. If a reported
$a$ is known to satisfy $|v-a|\leq\epsilon$, then $a-\epsilon\geq0$ suffices for
nonnegativity, while $a+\epsilon<0$ suffices for strict negativity. These are
ordinary bound consequences, not a choice of permanent evidence-state syntax.

This simple midpoint result assumes symmetric absolute error and no restriction
on the reported real number. Other loss functions, asymmetric consequences, or
requirements to return a feasible action instead of a numerical estimate define
different problems.

### F.2 Decision sufficiency can be much weaker

Fix a finite nonempty action set $A$. Each compatible model $\theta$ gives
scores $u_\theta(a)$ in common units. No distribution over compatible models is
assumed. Define the set of actions within $\epsilon\geq0$ of that model's best:

$$
A_\epsilon(\theta)=
\{a\in A:u_\theta(a)\geq\max_{b\in A}u_\theta(b)-\epsilon\}.
$$

A deterministic decision based only on the observed summary has regret at most
$\epsilon$ for every compatible model exactly when

$$
\bigcap_{\theta\text{ compatible}} A_\epsilon(\theta)\ne\varnothing.
$$

Necessity follows because the chosen action must lie in every such set.
Sufficiency follows by choosing any action in their intersection. The compatible
model family must be nonempty, consistent with E05. This is an example-level
acceptance criterion, not an implemented selection calculus.

For scores $(n,0)$ with any unknown integer $n\geq1$, the first action is optimal
in every compatible model. Exact best value cannot be recovered, and no finite
uniform numerical error is possible over this unbounded family, yet zero-regret
choice is immediate. Conversely, models with scores $(1,0)$ and $(0,1)$ have no
common $\epsilon$-optimal deterministic action for $\epsilon<1$.

Randomization changes the latter question when regret is evaluated in
expectation over an independent action draw. Choosing the first action with
probability $r$ gives regrets $1-r$ and $r$. Their worst value is minimized at
$r=1/2$, where it equals $1/2$. This does not guarantee realized regret at most
one half on every random draw. The execution and aggregation contract matters.

Current decision sufficiency is not automatically future sufficiency. In the
$(n,0)$ family, charging a new cost of two only to the first action makes the
second preferable for $n=1$ and the first preferable for $n=3$. A summary
retaining only the original winning action cannot answer that changed question.
No inference about all future tasks follows from success on the current one.

There is a sharp positive tolerance repair for that same cost change. Charge
any known $\kappa\geq0$ to the first action, giving scores $(n-\kappa,0)$ for
unknown integers $n\geq1$. Always choosing the first action has worst-case
regret

$$
\sup_{n\geq1}\max(\kappa-n,0)=\max(\kappa-1,0).
$$

Always choosing the second has unbounded worst-case regret as $n$ increases.
A fixed randomized choice that selects the second with any positive probability
also has unbounded worst-model expected regret. Thus the first action is the
unique finite-regret choice among these fixed randomized policies. It meets a
declared uniform regret tolerance $\epsilon$ exactly when
$\epsilon\geq\max(\kappa-1,0)$. In particular, the cost-two example has no
uniformly exact best action, but the original first action still guarantees
regret at most one. Failure of exact selection does not settle the pragmatic
question at nonzero tolerance. This uses the known lower bound $n\geq1$, not
just an unexplained label naming the previous winner.

### F.3 A useful approximate-score guarantee

Suppose a reported score vector satisfies the *simultaneous* error bound
$|u(a)-\hat u(a)|\leq\delta$ for every available action. Select an action
$\hat a$ maximizing $\hat u$, and let $a^*$ maximize $u$. Then

$$
\begin{aligned}
u(a^*)-u(\hat a)
&=[u(a^*)-\hat u(a^*)]
 +[\hat u(a^*)-\hat u(\hat a)]
 +[\hat u(\hat a)-u(\hat a)]\\
&\leq\delta+0+\delta=2\delta.
\end{aligned}
$$

The constant is sharp under only these bounds: predicted scores $(0,0)$ and
true scores $(-\delta,\delta)$ give regret $2\delta$ when the declared tie rule
selects the first action. An estimated winning margin greater than $2\delta$
also guarantees that this action is the unique true winner. At equality,
a true tie remains possible.

A marginal statistical statement about each separate action is not the
simultaneous deterministic premise used here. A common offset error can also
make the generic $2\delta$ bound conservative because comparisons cancel it.
Those are different information contracts, not counterexamples to the bound.

### F.4 Separate high-probability claims are not a simultaneous certificate

The simultaneous premise in F.3 cannot be replaced without adjustment by
high marginal coverage for each action. Let the reference scores be $u(0)=1$
and $u(i)=0$ for $i=1,\ldots,m$, where $m\geq2$. Generate a report by selecting
$I$ uniformly from $1,\ldots,m$, reporting $\hat u(I)=2$, and reporting every
other score exactly. The best action's score is always correct. For each
particular other action, its reported score is correct with probability
$1-1/m$. Yet the reported unique maximum is *always* a suboptimal action, so
greedy selection has regret one with probability one. Marginal coverage can
approach one as $m$ grows without repairing that selection claim.

A valid repair needs no independence assumption. Suppose events
$G_a=\{|u(a)-\hat u(a)|\leq\delta\}$ have failure probabilities at most
$\alpha_a$. The indicator of a union is at most the sum of the separate
indicators, so

$$
\Pr\left(\bigcap_a G_a\right)
\geq 1-\alpha,\qquad
\alpha=\min\left(1,\sum_a\alpha_a\right).
$$

On that event F.3 gives regret at most $2\delta$. The preceding example makes
the union-bound guarantee vacuous and the simultaneous event empty; it is not
a counterexample to this adjusted claim.

An expected-regret conclusion additionally needs control of failures. If the
reference score range has width at most $B\geq0$, regret is always at most $B$.
Putting $d=\min(B,2\delta)$ gives

$$
\mathbb E[\mathrm{regret}]
\leq (1-\alpha)d+\alpha B.
$$

This follows by splitting expectation between the simultaneous good event and
its complement; the bound increases with the failure probability because
$B\geq d$. Without a bound on failure losses, a small failure probability alone
does not bound expected regret. These are finite constructed reporting laws,
not a calibration result for a learned estimator or a diagnosis of phase one.

**Requirement refined.** F02 should distinguish exact score recovery, adequate
numerical precision, and sufficient information for the declared decision.
Pragmatic tolerance must enter the requested guarantee, rather than be replaced
silently by a demand to reconstruct everything exactly. Regret is one optional
way to express that tolerance, not a required universal primitive.

## G. The observation schedule belongs to the question

A finite generalization checks E08's quantifier order. Let $p(w,s)$ be a declared
joint probability table over hidden scenarios $w$ and observable signals $s$.
Let $A$ be a finite nonempty action set with payoffs $u(w,a)$. A policy may use
$s$ and independent randomization, but not unobserved $w$. With zero acquisition
cost for this comparison, the optimal values are

$$
V_0=\max_a\sum_{w,s}p(w,s)u(w,a),
$$

$$
V_S=\sum_s\max_a\sum_w p(w,s)u(w,a),
\qquad
V_*=\sum_w\left(\sum_s p(w,s)\right)\max_a u(w,a).
$$

The signal formula follows by choosing one action separately for each observed
signal; its inner sum is unnormalized, so zero-probability signals cause no
conditional division. Randomized choices cannot improve a maximum of a linear
payoff over a finite simplex. Ignoring the signal is allowed, and a hidden-state
oracle has at least as many choices, giving

$$
V_0\leq V_S\leq V_*.
$$

The upper equality has an exact finite condition: for every signal of positive
probability, there must exist a single action maximizing $u(w,a)$ for *all*
scenarios with $p(w,s)>0$. Indeed, for a signal-dependent maximizing action
$a_s$, the gap is a sum of nonnegative terms

$$
\sum_{w,s}p(w,s)[\max_a u(w,a)-u(w,a_s)].
$$

It vanishes exactly when every positive-weight term vanishes. In E08, genuinely
noisy signals leave both scenarios possible and the scenarios have different
unique best actions, so the unattainable upper envelope remains strictly above
the signal value. Perfect signals remove that obstruction.

A related check separates worst-case expected value from realized guarantees.
With E08's two actions and no observation, choose $X$ with probability $r$.
Conditional on the hidden scenario, the expected payoffs are $4r-1$ and $3-4r$.
Their minimum is

$$
1-4|r-1/2|,
$$

maximized at value one by $r=1/2$. Every deterministic action instead has
worst-scenario payoff $-1$. Nevertheless every randomized policy also admits a
realized action/scenario pair with payoff $-1$. Treating the random seed as an
additional scenario therefore gives a different guarantee. An adversary allowed
to observe the realized action before choosing the scenario likewise changes
the information schedule.

**Requirement refined.** Moving a maximum, minimum, or expectation across another
operator can change which information is available and when a choice occurs.
An algebraic operation needs an operational interpretation, not just a familiar
name. These checks do not launch the deferred inquiry-policy project.

## H. A current summary need not survive an evidence update

Take two possible joint laws for payoff $X$ and an observed binary signal $S$:

```text
P: probability 1/2 on (-1,0), probability 1/2 on (1,1)
Q: probability 1/2 on (-1,1), probability 1/2 on (1,0)
```

Both give the same complete payoff marginal, the same signal marginal, and
current expected payoff zero. After observing $S=1$, however,

$$
\mathbb E_P[X\mid S=1]=1,
\qquad
\mathbb E_Q[X\mid S=1]=-1.
$$

Consequently current evaluation, even supplemented by both separate marginal
laws, does not determine this updated evaluation. The same information-access
qualification as E03 applies: access to the actual joint law would remove the
ambiguity. For a specified event $A$, the two statistics

$$
b=\mathbb E[X\mathbf1_A],\qquad p=\Pr(A)>0
$$

suffice for this one update, giving $m=b/p$. This neither establishes cheap
acquisition nor closure under an unlimited sequence of future updates.

A precision check is instructive. If $|X|\leq M$ on the admitted scenarios,
$|b-\hat b|\leq\delta_b$, $|p-\hat p|\leq\delta_p$, and both probabilities in
the displayed ratios are positive, then

$$
\left|\frac{\hat b}{\hat p}-\frac b p\right|
=\frac{|\hat b-b+m(p-\hat p)|}{\hat p}
\leq\frac{\delta_b+M\delta_p}{\hat p}.
$$

Thus a declared lower bound on the denominator supplies a stability guarantee.
The positive-event premise must be justified; the formula cannot authorize
conditioning on a zero-probability event simply because a point estimate of its
probability is positive.

There is no comparable uniform small-change guarantee without controlling the
conditioning event. For any rational $0<t<1$, let $P_t$ put mass $t$ on $(1,1)$
and $1-t$ on $(0,0)$, and let $Q_t$ put mass $t$ on $(-1,1)$ and $1-t$ on
$(0,0)$. Half the sum of absolute differences between their probability tables
is $t$. Their event probabilities both equal $t$, yet their conditional means
are one and minus one. An arbitrarily small pre-update discrepancy can therefore
produce a conditional-mean gap of two. The means remain bounded; it is uniform
stability of the update that fails, not finiteness of the updated score.

**Requirement refined.** A claim that a summary is adequate now must identify
which later context changes, compositions, or evidence queries it supports.
When approximate information is propagated, sensitivity can depend on the event
or operating range. This is a requirement to state the contract, not a demand
to encode every possible future observation in advance.

## I. Pairwise compatibility versus a common approximate model

This extends E05's conflict test without declaring that every local model must
share a single global interpretation. The request here explicitly identifies
three binary quantities $A,B,C$ across three observation contexts and asks for
one joint probability law. Each local model has uniform one-bit marginals and
requires a pair relation:

$$
A=B,
\qquad B=C,
\qquad A\ne C.
$$

Every two requirements have a joint realization with uniform single-bit
marginals. All three do not: the first two equalities imply $A=C$.
The one-variable overlap marginals match, so matching those overlaps does not
establish global compatibility. If the symbols denote different quantities in
different contexts, that identification premise is absent and this contradiction
does not follow. The result blocks the requested common model, not all local use.

### I.1 An exact error-budget calculation

For a possible triple define the violation indicators

$$
e_1=\mathbf1_{A\ne B},\quad
e_2=\mathbf1_{B\ne C},\quad
e_3=\mathbf1_{A=C}.
$$

The eight assignments split into four complementary pairs:

| Assignments | $(e_1,e_2,e_3)$ |
|---|---|
| $000,111$ | $(0,0,1)$ |
| $001,110$ | $(0,1,0)$ |
| $011,100$ | $(1,0,0)$ |
| $010,101$ | $(1,1,1)$ |

Every row violates at least one requirement. Thus any joint law has
$\mathbb E e_1+\mathbb E e_2+\mathbb E e_3\geq1$. If the allowed error caps
are $\epsilon_i\in[0,1]$, feasibility requires

$$
\epsilon_1+\epsilon_2+\epsilon_3\geq1.
$$

This condition is also sufficient. Put $S=\epsilon_1+\epsilon_2+\epsilon_3$
and $w_i=\epsilon_i/S$ when $S\geq1$. Choose the complementary pair with
exactly violation $i$ with probability $w_i$, then choose either member of that
pair with probability one half. Each bit is uniform, and

$$
\mathbb E e_i=w_i\leq\epsilon_i.
$$

Thus the displayed sum condition exactly characterizes the feasible error caps
for this example. With equal caps, the threshold is $\epsilon=1/3$.
Uniform probability on $000,111,001,110,011,100$ attains equality. Caps strictly
below one third for all three relations are impossible.

The conclusion also applies when the error contract compares each full pair
law with its prescribed uniform equality/inequality law using half the sum of
absolute cell differences. Necessity follows because the target law puts zero
mass on a violation event, and its probability under a proposed law is bounded
by that distance. In the constructed law, the correct-relation cells each have
mass $(1-w_i)/2$ and the two violating cells each have mass $w_i/2$, so the
distance is exactly $w_i$. No independence assumption is used.

Additional assumptions can change the answer. If the uniform bits are required
to be pairwise independent, each relation is violated with probability $1/2$;
the best equal cap in that narrower class is $1/2$, not $1/3$. The one-third
construction is correlated. Also, this is an *existence* result for a model
fitting the supplied local specifications. It is not a guarantee that every
compatible joint model has those errors, nor empirical evidence that the
constructed joint model predicts an external population correctly.

### I.2 Exact errors occupy a smaller region than upper caps

Write $r_i=\mathbb E e_i$ for exact violation probabilities. Let $t$ be the
probability of the triple-violation pair and let $w_i$ be the probability of
the pair with only violation $i$. The table implies

$$
r_i=w_i+t,\qquad w_1+w_2+w_3+t=1.
$$

Summing the first equations and substituting the second gives the uniquely
required pattern weights

$$
t=\frac{r_1+r_2+r_3-1}{2},
\qquad
w_i=\frac{1+2r_i-(r_1+r_2+r_3)}{2}.
$$

Consequently an exact vector is realizable precisely when all four displayed
weights are nonnegative. Their sum is then one, so choosing each complementary
pair with its assigned probability and symmetrizing within the pair realizes
it with uniform one-bit marginals. Conversely, every joint law induces these
nonnegative weights by grouping its eight assignments. This proves both
necessity and sufficiency, without inferring sufficiency from sampled laws.

For $r_i\in[0,1]$ the equivalent inequalities are

$$
r_1+r_2+r_3\geq1,
\qquad
r_j+r_k-r_i\leq1\quad\text{for each distinct }i,j,k.
$$

The upper-cap criterion in I.1 requires only that *some* such vector satisfy
$r_i\leq\epsilon_i$. It does not require the cap vector itself to be realizable.
For example, exact $(1,1,0)$ would require $t=1/2$ and $w_3=-1/2$, so it is
impossible. Nevertheless caps $(1,1,0)$ are feasible using exact $(1,0,0)$.
The latter requires $t=0,w_1=1,w_2=w_3=0$ and is realized by equal mass on
$011,100$. Exact matching and meeting tolerances are different queries.

### I.3 Which approximate repair is preferable depends on the task

Equal maximum-error control minimizes $\max_i r_i$. The lower bound
$\sum_i r_i\geq1$ forces this maximum to be at least $1/3$, attained by the
symmetrized mixture with $r=(1/3,1/3,1/3)$.

A different declared objective may charge nonnegative costs $c_i$ for the three
kinds of violation and minimize $\sum_i c_i r_i$. Every realization is a
mixture of the four table patterns. Their costs are $c_1,c_2,c_3$, and
$c_1+c_2+c_3$, so the least achievable cost is exactly

$$
\min(c_1,c_2,c_3).
$$

It is attained by concentrating on the complementary pair with the cheapest
single violation. For costs $(1,2,3)$, exact errors $(1,0,0)$ cost one, whereas
the equal-error solution costs two. The equal-error solution instead has the
better maximum error. Neither comparison selects an objective for the project;
it shows why a claim of the “best repair” must specify its aggregation. These
cost conclusions assume nonnegative weights and no additional upper caps.

All three local errors in this calculation are measured under marginals of
one requested joint population. Context-dependent sampling populations or
context-dependent copies of the symbols define another problem. The finite
contradiction and its quantitative repair do not establish that every practical
family of local models must admit this joint identification.

**Requirement refined.** Local agreement, existence of a common model, exact
matching, and acceptable approximation are distinct obligations. An impossibility
at zero tolerance need not defeat a useful positive result at declared nonzero
tolerance. Conversely, numerical tolerances need an actual compatibility proof;
“approximately consistent” is not a free pass. These are finite diagnostic
examples, not a chosen global-consistency requirement for Value Logic.

## J. “Small error” must identify its aggregation

### J.1 Uniform, mean-absolute, and mean errors

E03's bottleneck also separates three commonly conflated error statements.
For real tuples $x,y$ of the same finite length,

$$
|\min_i x_i-\min_i y_i|\leq\max_i|x_i-y_i|.
$$

To see this, let $d=\max_i|x_i-y_i|$. Each $x_i$ is between $y_i-d$ and
$y_i+d$; taking minima preserves these two bounds. Therefore uniform
componentwise error bounds $|X_i(w)-\hat X_i(w)|\leq\delta_i$ on a shared
scenario scope give a uniform bottleneck bound of $\max_i\delta_i$.

If only mean absolute errors are available under the same declared weighting,
then instead

$$
\mathbb E|\min_i X_i-\min_i\hat X_i|
\leq\mathbb E\max_i|X_i-\hat X_i|
\leq\sum_i\mathbb E|X_i-\hat X_i|.
$$

Replacing the final sum by the maximum of the separate mean errors is generally
invalid. On $n$ equiprobable scenarios let every ideal payoff be zero, and let
approximation $i$ equal $-n\delta$ only on scenario $i$ and zero elsewhere.
Each mean absolute error is $\delta$, but the minimum is constantly
$-n\delta$, so its mean absolute error is $n\delta$. The sum bound is attained.
For two inputs, this already gives a factor-two counterexample.

Finally, an error bound on the *mean value*,
$|\mathbb E X-\mathbb E\hat X|$, is weaker still than a mean absolute error.
The inequality

$$
|\mathbb E(X-\hat X)|\leq\mathbb E|X-\hat X|
$$

follows by the triangle inequality for finite sums, but has no converse with a
finite constant over unrestricted examples: use $X=(M,-M)$ and $\hat X=(0,0)$.
The left side is zero and the right side is $M$.

**Requirement refined.** A rule justified for uniform error cannot inherit the
same coefficient under average error or error of an average. The same numeric
$\delta$ can denote different facts. Joint alignment, the relevant input norm,
and the task loss aggregation must remain available to the consumer; this does
not require any specific representation of them.

### J.2 A mean sensitivity cannot replace a uniform sensitivity

A further check joins E03's information issue to E04's sequential rule. Applying
the valid pointwise rule with case-dependent quantities gives

$$
|\hat g(\hat f(w))-g(f(w))|
\leq\eta(w)+K(w)\delta(w).
$$

Averaging therefore yields $\mathbb E\eta+\mathbb E[K\delta]$ as an upper bound,
not generally $\mathbb E\eta+(\mathbb E K)(\mathbb E\delta)$. The latter would
need extra joint information. These expressions can have the same units and
still encode different claims.

Here is a single fixed downstream map that makes the distinction explicit.
Take $n\geq3$ equiprobable inputs $w=1,\ldots,n$. Set $f(w)=0$, let the
upstream approximation be $\hat f(w)=\delta(w)\geq0$, and take
$g(u)=\hat g(u)=u^2$. There is no downstream approximation error. On the
case-specific interval $[0,\delta(w)]$,

$$
|u^2-v^2|=|u-v|(u+v)\leq2\delta(w)|u-v|,
$$

so $K(w)=2\delta(w)$ is a valid local Lipschitz bound. When $\delta(w)=0$,
the interval is a singleton and the zero bound is valid. The exact composite
absolute error is $\delta(w)^2$.

Compare two upstream-error profiles on the same $n$ cases:

| Profile | $\mathbb E\delta$ | $\mathbb E K$ | Exact mean composite error |
|---|---:|---:|---:|
| $\delta(w)=1$ on every case | $1$ | $2$ | $1$ |
| $\delta(1)=n$, $\delta(w)=0$ for $w>1$ | $1$ | $2$ | $n$ |

The product of the two displayed means is two in both profiles. It is not an
upper bound for the spiked profile. The correctly averaged bound is
$\mathbb E[K\delta]=2\mathbb E\delta^2$, so no valid pointwise rule has failed:
the invalid step was changing the aggregation.

There is a useful sharp range when more information is available. If a profile
satisfies $0\leq\delta(w)\leq n$ and $\mathbb E\delta=1$, then

$$
1\leq\mathbb E\delta^2\leq n.
$$

For the lower bound, average $(\delta-1)^2\geq0$ and use the supplied mean.
For the upper bound, use $\delta^2\leq n\delta$ pointwise. Every intermediate
value is attained on the same finite population: for $0\leq t\leq1$, take

$$
\delta(1)=1+(n-1)t,
\qquad \delta(w)=1-t\ (w>1).
$$

The mean remains one, while expansion gives
$\mathbb E\delta^2=1+(n-1)t^2$. Thus the two profiles are endpoints of a sharp
answer interval, not isolated numerical anomalies. These are exact real-valued
profiles; rational test values of $t$ check selected points, not all reals.

**Requirement refined.** A uniform sensitivity bound, a mean of local
sensitivities, and the joint mean of sensitivity times error are different
premises. A rule may use a supported global bound or the joint product statistic;
it cannot silently replace either by a product of separate averages. The
quantity being summarized and the scope of its certificate matter even after
all units are correct. This does not mandate one error norm or one calculus.

## K. Finite observations do not certify an unbounded tail

This checks the evidence scope of E07 rather than disallowing unbounded value.
Keep its declared probabilities $p(k)=2^{-k}$ on positive integers. Suppose an
interface reveals a nonnegative loss only for $k\leq N$, where $N\geq1$, and
reveals no upper envelope for later values. Compare

$$
L_0(k)=k,
\qquad
L_M(k)=k+M2^{N+1}\mathbf1_{\{k=N+1\}},\qquad M>0.
$$

The two losses agree on every revealed input, and each has finite expectation.
Nevertheless

$$
\mathbb E L_0=2,
\qquad
\mathbb E L_M=2+2^{-(N+1)}M2^{N+1}=2+M.
$$

Thus any finite revealed prefix leaves the full expected loss unbounded over
this admitted family. Every member is integrable; requiring integrability
alone does not supply a *uniform* upper bound over the compatible family.
For a tolerance of three, taking $M>1$ gives opposite adequacy answers from the
same finite input record. This is an information restriction, not an empirical
claim that any particular physical model has such a tail.

Squashing every loss with E07's $h$ does not repair that real-unit question.
The two transformed objects differ at only the exceptional input, where their
code difference lies strictly between zero and one. Hence

$$
0<\mathbb E h(L_M)-\mathbb E h(L_0)<2^{-(N+1)},
$$

even while their original expected losses differ by an arbitrarily large $M$.
A task that *actually values* $\mathbb E h(L)$ is a different task from one
that uses $h$ only as an internal encoding and still needs $\mathbb E L$.
Neither interpretation is ruled out, but they cannot be silently identified.

There is a positive repair with an explicitly supported envelope. Suppose
$0\leq L(k)\leq Ck$ for all $k$, with known $C\geq0$. Shifting the geometric
series gives

$$
\begin{aligned}
\sum_{k>N}k2^{-k}
&=2^{-N}\sum_{j\geq1}(N+j)2^{-j}\\
&=2^{-N}(N+2).
\end{aligned}
$$

If the prefix contribution is $a_N=\sum_{k=1}^N L(k)2^{-k}$, then

$$
a_N\leq\mathbb E L\leq a_N+C(N+2)2^{-N}.
$$

This is sharp for the stated class: the same fixed prefix can be extended with
zero tail or with $Ck$ tail. For $C=1,N=8$ and prefix $L(k)=k$, the known
contribution is $251/128$ and the maximum tail is $5/128$, yielding the interval
$[251/128,2]$. Adequacy at tolerance two follows from the upper bound; exact
expectation does not follow unless the whole function has also been specified.

A claimed envelope needs its own premises. It is not established by agreeing
with observed cases. In the original fully specified $L(k)=k$ example, the
infinite formula is already a premise and permits direct calculation. The
finite-prefix example deliberately removes that information. Its negative
result therefore does not invalidate the original series calculation.

**Requirement refined.** Distinguish a declared complete model, finite checked
outputs, and a class-wide tail certificate. A finite expected value of each
compatible model need not yield a useful common error bound. A supported
integrable envelope can restore a quantitative guarantee without imposing a
bounded value carrier.

## L. Audit disposition and remaining scope

The original eight examples survive reconstruction with explicit refinements:
E06 is about interpreted specifications and residue-only interfaces; E07's
finite-range precision bound needs a range condition on the decoded estimate;
and new exact-versus-upper-bound distinctions are recorded wherever used.
Sections B–K add positive controls and separating witnesses rather than select a
semantic carrier. The sharp one-third compatibility threshold and the tolerance-
aware decision examples make pragmatic error tolerance an explicit test, not
merely introductory motivation.

### L.1 Metatheory and admissible conclusions

The finite calculations use ordinary ordered arithmetic, finite sums and
finite choices. Many rational fixtures are completely reproducible using
integer fractions. The infinite statements identify the additional step:
E07 and K use the stated geometric series and its vanishing remainder; E.1
uses rational density in the usual Archimedean real order; F.1's infinite-fiber
version uses real infima and suprema. No invocation of an unrestricted axiom
of choice or an unexamined probability representation theorem occurs in these
arguments. This describes the displayed proofs, not an independence theorem
about their weakest possible foundations.

Using those mathematical premises does not certify their metaphysical status.
Nor do properties of real numbers become mandatory axioms of value objects.
For example, E.1 concerns recodings into ordinary real arithmetic; it says
nothing by itself about every possible ordered algebra. E06 supplies interpreted
finite structures rather than a proof that one axiomatic system is universally
best. The later candidate comparison remains responsible for deciding which
mathematical assumptions and operations it actually needs.

### L.2 What the reconstruction does and does not settle

The numerical fixtures in `../checks/f01_reconstruction.py` are development
checks, not the F11 reasoner or the F14/F15 frozen challenge. General statements
above rest on the displayed arguments, not on the number of passing tests.
The narrow [source check](../work_logs/F01_2026-09-21_S2_sources.md) identifies
relevant quantitative-algebra assumptions without importing a completeness
result or claiming novelty. A later candidate may adopt a smaller query family;
it must state that restriction and what practical capability is lost.
