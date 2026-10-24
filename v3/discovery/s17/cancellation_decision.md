# A block-informed decision beyond old-vector cancellation ambiguity

Codex (GPT-6), October 24, 2026 UTC. DEVELOPMENT; algebraically selected
example for the same N16-C/v1 contribution event. It supplements the earlier
0.5385 example and its approximately 1.80% strong-control width gain.

## Prospective construction and question

Use the canonical two-by-two source M=diag(40,1/3), target
v=(1,1)/sqrt(2), C=diag(1/1601,9/10), edit radius e=3 and threshold 3/5.
Check the existing rational verifier using C_minus=C-10^-4 I,
C_plus=C+10^-4 I, V=vv^T, E=9, t_lower=10 and t_upper=100.
The question is whether this rounded block certifies F(N;v)<3/5 for every
compatible edit, while the entire old optimizer and residual still permit
a full-rank alternative source whose edited objective is exactly one.

The selection comes from a structural difference. For s=v^T S v,
m=||Sv||^2 and q=s-m>0, the rank-one source compatible with the old vectors
can cancel the target once E>=(1-s)^2/q. In contrast, for the canonical
full block the cancellation threshold is c^T(C^(-1)-I)c. Strong anisotropy
can separate these two budgets substantially. This is why the displayed
parameters were chosen; they are not a fresh statistical test population.

## Exact same-vector alternative

Write u=(1,1), w0=(1/1601,9/10) and x0=(40/1601,3/10), all unnormalized
by sqrt(2). Then the actual old residual and optimizer are w=w0/sqrt(2)
and x=x0/sqrt(2), and q=||x0||^2/2. Set

    A0=(u-w0)x0^T/(2q),
    a=(w0_2,-w0_1), b=(x0_2,-x0_1),
    A=A0+(1/10)ab^T.

The added term annihilates x0 and its transpose annihilates w0. Thus
A x0=u-w0 and A^T w0=x0, proving the same old optimizer and residual.
The determinant is q/5>0, so A is full rank and its full resolvent is
strictly between zero and identity. Define

    Delta=-(1/2)u(A^T u)^T, N=A+Delta.

Then N^T u=0, and F(N;v)=1. Its squared edit norm is

    ||Delta||op^2=||A^T u||^2/2
      =(1-s)^2/q+(q/100)(w0_2-w0_1)^2.

The focused exact check will verify that this is below 9, together with
the normal equations and the rounded-block verdict. This alternative is
excluded by the extra block observations. Both sources and both old-vector
representations use the same two-by-two dimensions and the same target.

## Information and decision meaning

The action is to approve all norm-budgeted edits of a partly retained model
as having reoptimized loss below 3/5. The block can support approval if the
checker passes. Old vectors alone cannot support it because the displayed
compatible alternative reaches loss one. An actual known source, additional
spectral warrants, or a particular edit direction could change the comparison.

The rounded block can be obtained by the established three-query polarization
adapter with scalar half-width epsilon=1/25000, since its matrix half-width
is (5/2)epsilon=1/10000. This is an explicitly paid information difference.
It does not imply that every solver must buy three queries or that the
additional observations are economical for every workload. The ordinary
same-block SDP and the identical rational implementation tie the guarantee.

## Observed exact result

[cancellation_check.py](cancellation_check.py) and
[cancellation_result.json](cancellation_result.json) passed the specified
checks. The rounded-block upper certificate is

    82419925705279100 / 141343212714434881
      = 0.583119090916... < 3/5.

The full-rank same-vector alternative has edit squared norm approximately
6.668706704, strictly below the allowed 9, and its new objective is exactly
1. Thus the sharp upper guarantee from those old vectors alone is 1,
whereas the declared rounded block certifies less than 0.584. The proof
and recorded fractions, not the decimal approximations, establish the result.
The exact check took 587,000 ns on the recorded runtime.

This makes the contribution's decision consequence less dependent on a tiny
threshold gap. It does not establish the novelty of the sharp endpoint
theorem: the successful decision only needs its valid upper bound, which
also follows from standard variational inequalities. The useful proposed
synthesis combines that certificate with a sharp account of decisions that
the specified information cannot settle. Its prior-art uncertainty remains.

## A genuinely compressed version with the same known source norm

The two-dimensional example does not require the actual source to be small.
Take M_big=diag(40,1/3,40) and A_big=diag(A,40), W=[e_1,e_2],
and v=W(1,1)/sqrt(2). The complete old residual and optimizer from both
sources append one zero coordinate to the vectors above. The same edit,
padded by zeros, still cancels the target for A_big, while the retained
two-dimensional block for M_big is unchanged. Arbitrarily many decoupled
coordinates can be appended in the same way. All norm-budgeted edits,
including ones coupling these coordinates, remain covered by the block bound.

Even the source operator norm can be disclosed equally to both comparisons.
For the displayed A, ||A0||^2=||u-w0||^2/||x0||^2 < 101/9 < (7/2)^2.
Also ||w0||<1 and ||x0||<1, so ||(1/10)ab^T||<1/10 and ||A||<18/5.
Thus both enlarged sources have operator norm exactly 40. Their edit budget
3 can equivalently be described as the same relative allowance 3/40 of
that disclosed norm. The full old vectors plus this operator norm still
admit the cancellation alternative. No new experiment is needed for this
direct-sum construction; it follows from the exact normal equations and
the displayed elementary norm bounds.

The numerical diagonal form is a construction, not public structural
information granted to a comparison. A warrant that the unknown source
must remain diagonal would be an additional premise and could eliminate
the alternative. This example claims neither that all structured sources
need the block nor that its extra observations always pay for themselves.
