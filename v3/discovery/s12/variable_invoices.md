# Variable-length invoices can reduce the average acquisition surcharge

Codex (GPT-6), s12 DEVELOPMENT. A constructive direction, with no all-policy
optimality claim yet. Same no-repeat, same-world private-reset interface as
[parity_price.md](parity_price.md). Initially n>=2 independent fair hidden bits,
unit coordinate fees, cap 2<=H<=n, and initially zero episode overhead.
The public side sees only each exact integer invoice.

## Prefix stopping rather than fixed parity blocks

At a public state with k unknown bits, set m=min(k,H-1). Query a fixed ordered
list of these m bits, stopping at the first zero. If all m bits are one, buy
one further distinct coordinate as a marker and stop. Such a marker always
exists since m<=H-1<=n-1; it may be known from a previous episode, or may be
another still-unknown coordinate whose answer is discarded.

An invoice j<=m identifies exactly j-1 initial ones followed by zero. Invoice
m+1 identifies m ones. Thus this episode publicly learns j or m bits,
respectively, and the unknown remaining bits are still independent and fair.
Repeat until none remain. This recovers the full vector, hence any function
of it, rather than just a parity. It spends one extra purchase only on the
all-ones branch. The private answer to that marker does not become public.

Let R_k be expected purchases in excess of the k newly learned bits, with
R_0=0. The exact recursion is

```math
R_k=\sum_{j=1}^{m}2^{-j}R_{k-j}
       +2^{-m}(1+R_{k-m}),\qquad m=\min(k,H-1).
```

The last residual appears twice because the final zero and all-ones events
both learn m bits. For 1<=k<=H-1, R_k=1/2 by induction. At k=H,
R_H=1/2+2^{-(H-1)}. For H=3 the recurrence solves to

```math
R_k=\frac{k}{6}+\frac{2}{9}\left(1-(-1/2)^k\right).
```

For example n=3,H=3 uses expected invoice 3.75. Fixed parity blocks of sizes
two and one use expected invoice 4, while their hard worst-case optimum is 5.
The variable procedure still has worst invoice n+ceil(n/(H-1)) when f=0:
every marker except possibly the final one publicly resolves H-1 new bits,
so there are at most ceil(n/(H-1)) markers, with equality on the all-ones
world. It therefore improves the fixed-block average while retaining the
optimal parity worst-case bill in this unit-price, zero-overhead setting.
The first draft left this worst-case comparison unresolved; the pathwise
marker count settles it without an experiment.

For fixed H and large k, the recurrence has linear slope
1/(2^H-2). One full-length episode learns on average
2*(1-2^{-(H-1)}) bits and has expected extra purchase 2^{-(H-1)};
the exact recurrence gives R_k=k/(2^H-2)+O_H(1). For a direct proof, put
d=H-1, a_j=2^(-j) for j<d and a_d=2^(1-d). These coefficients sum to one
and have mean mu=2*(1-2^(-d)). For k>=d, R_k=2^(-d)+sum_j a_j R_(k-j).
Subtract beta*k, beta=2^(-d)/mu. The remainder is a convex combination of
previous remainders and hence stays between the extrema of the finite initial
list. No asymptotic independence or unproved renewal-rate claim is needed.
This contrasts with fixed parity blocks' surcharge about k/[2(H-1)].
The statement is a construction comparison, not a lower bound on other
expected-cost procedures, nor a claim of learning the bit distribution.

## Episode overhead and information limits

Let N_k be the expected episode count. It obeys N_0=0 and

```math
N_k=1+\sum_{j=1}^{m}2^{-j}N_{k-j}+2^{-m}N_{k-m}.
```

With known overhead f, this policy's expected invoice is k+R_k+f*N_k.
In fact N_k=k/2+R_k exactly: each zero publicly learned ends one episode,
and every other episode ends with a marker. All k bits are eventually learned,
so the expected number of zero-ending episodes is k/2.
Its asymptotic episode slope is 1/[2*(1-2^{-(H-1)})], much larger than
fixed blocks' approximately 1/(H-1). Therefore a positive reset/setup price
can remove the advantage. The controller can choose a shorter m, another
orientation or a different policy, but each such optimization needs its own
claim. For fixed d>=2, its asymptotic average beats fixed blocks precisely when
f*[d-2+2^(1-d)] < 1-(d+1)*2^(-d). At H=3 this is f<1/2. This comparison
does not optimize over mixtures or other programs. The prefix policy's exact
hard-worst bill for k>=1 is
k+1+f*k+floor((k-1)/d)*max(0,1-f*(d-1)): maximize the number of full marker
episodes if their extra marker offsets the episode savings, then use
one-bit zero-ending episodes and a final one-bit marker episode. Any
zero-ending episode learning more bits can be split to increase or preserve
the bill. A final marker of more than one remaining bit can similarly be
replaced by zeros and one final marker. Thus nonzero overhead can make the
prefix worst bill larger than the fixed-block worst bill.
Exact readout and uniform independent remaining bits are assumptions,
not consequences of observing low invoices.

Prospective cheap screen: reuse the frozen unrestricted three-bit private
program enumerator, add an exact expected-cost Bellman oracle for parity and
full-vector recovery, and compare this explicit policy and fixed blocks.
Inspect primary variable-cost coding / cost-observation literature before
asserting a new algorithmic principle.

## First finite screen and a better parity-specific continuation

[variable_probe.py](variable_probe.py), unchanged first run with bundled Python
3.12.14, passed 36,868 explicit hidden-world executions and 275 hard-cost
formula checks (n=2 through 11, every admissible cap, five overheads). Its
30 unrestricted expected-cost oracle panels for n=3/cap 2 or 3 and n=4/cap 3
all completed within their 20,000-state limit. The combined probe took
5.1732254 seconds. These are finite DEVELOPMENT checks.

At overhead zero, the unrestricted oracle agrees with prefix recovery for
both parity and the full vector: 15/4 at n=3,H=3 and 39/8 at n=4,H=3. Against
fixed parity blocks, those are acquisition reductions of 6.25% and 2.5%, with
the same respective worst bills 5 and 6. An ordinary identical code ties.

With positive overhead, full-vector recovery can be unnecessary. When k<=H-1
bits remain, one parity-block episode has the same expected acquisition
surcharge 1/2 as prefix recovery but fewer episodes. Substituting this terminal
rule preserves the query-count recurrence R_k and lowers the episode count.
For n=3,H=3 it gives expected cost 15/4+2f, agreeing with the unrestricted
parity oracle at all five tested overheads. It uses exactly two episodes on
every world. For n=4,H=3 it gives 39/8+(5/2)f; fixed blocks beat that formula
when f>1/4. Thus the fixed prefix rule is not generally expected-optimal.

A restricted synthesis can choose, at every k, between a parity block and a
prefix stop of length 1<=m<=min(k,H-1). Let U_0=0 be the expected excess cost
over the remaining k data purchases, including episode overhead. Then

```math
U_k=\min_m\left\{\tfrac12+f+U_{k-m},\quad
  2^{-m}+f+\sum_{j=1}^{m}2^{-j}U_{k-j}+2^{-m}U_{k-m}\right\}.
```

This dynamic program is exact only within the declared hybrid class and uses
O(nH) arithmetic operations with prefix-weighted sums or direct O(nH^2)
evaluation. It is an upper bound for unrestricted private programs. The oracle
does not yet prove that this class is sufficient for larger n or caps.

## No probability distribution on mathematical truth is required

Before execution, choose independent fair public mask bits r_i. Run the
construction on y_i=x_i xor r_i by flipping each privately obtained data bit
before its stopping test. Decode x by undoing the mask, or correct the final
parity by parity(r). For every fixed hidden x, y is uniform on the full cube.
Consequently the displayed expected acquisition costs hold for **every fixed
input**, averaging only over the procedure's own randomness. Correctness is
exact on every random tape; the pathwise worst bill is unchanged. This turns
the uniform-input construction into a zero-error randomized acquisition rule,
without assigning probabilities to unresolved mathematical truths.

The mask generation and use are real controller work: n independent random
bits and corresponding bit operations in the simple implementation. Fixed
parity blocks can likewise randomize marker orientation with only one coin
per block, obtaining their n+ceil(n/(H-1))/2 expected query bill on every x.
Thus the comparison gives a fee gain, not a demonstrated complete computation
gain. Short pseudorandom seeds do not automatically preserve the exact claim.

More generally, for parity or full-vector recovery on a full cube, the minimum
worst-input expected bill over zero-error randomized procedures equals the
minimum uniform-input expected bill over deterministic procedures. Lower:
average any randomized procedure over uniform x, interchange the finite
expectations, and bound each deterministic tape by the latter infimum. Upper:
uniformly mask any deterministic procedure approaching that infimum. The
known output translation preserves the requested task and every query price.
The same argument works on a checked affine source x0+V using a uniform mask
from V and the corresponding output offset. It does not automatically work
for arbitrary functions lacking that translation symmetry.

This is the ordinary minimax/distributional symmetrization argument, adapted
to this interface. It transfers the small exact oracle values to small
randomized minimax values; it does not transfer a finite oracle proof to
arbitrary dimension. Primary attribution and the original-paper access limit
are recorded in [literature.md](literature.md).
