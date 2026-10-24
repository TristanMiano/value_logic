# A finite-source precision obstruction

Codex (GPT-6), October 24, 2026 UTC. DEVELOPMENT. This supplies an
explicit realization for [precision.md](precision.md)'s conditioning
warning, entirely within 0<C<I. It is a consequence of the information
problem, not a new empirical speedup or an enlargement of N16-C/v1.

Let R>=8, E=1, c=(1,1)/sqrt(2), W=I, and define

    M_A=diag(R,R^(-2)), M_B=diag(R^2,R^(-2)),
    C_A=diag(1/(1+R^2), R^4/(1+R^4)),
    C_B=diag(1/(1+R^4), R^4/(1+R^4)).

Both sources are finite and invertible. Their retained-block distance is

    delta=(R^4-R^2)/[(1+R^2)*(1+R^4)] <= R^(-2).

Apply Delta_A=[[0,0],[-1,0]], which has operator norm one. Put q=R^2.
Direct inversion of I+(M_A+Delta_A)(M_A+Delta_A)^T gives

    F_A=[q+3+q^(-2)+2R]/[2*(q+2+(q+1)/q^2)].          (W1)

In particular F_A>=1/2+1/(2R). To check the inequality, subtract 1/2,
multiply its positive denominator, and use

    R^2+R-2-R^(-1)-R^(-2)-R^(-4) > 0  (R>=8).

For source class B, choose t=q+1 in the core upper envelope. Its second
eigenvalue is less than one, while its first is 1/(1+q^2). Monotonicity
and d>=0 therefore give

    U_B <= (q+2)/(2*q^2) + (q+1)/(2*q)
         = 1/2+1/q+1/q^2.

Thus

    u(C_A)-u(C_B) >= F_A-U_B
      >= 1/(2R)-1/R^2-1/R^4 >= 1/(4R) >= sqrt(delta)/4.   (W2)

The penultimate inequality follows from 1/R+1/R^3<=1/4 for R>=8.
This proves a square-root obstruction on strictly interior blocks using
actual source/edit witnesses. No singular limiting source, numerical
optimizer or sharpness theorem is needed for W2: an explicit feasible
value on A and a valid universal upper bound on B suffice.

At a threshold between these two values, the B block certifies that every
allowed edit stays below it, whereas the A block cannot truthfully do so.
Their common second diagonal entry and very close first entries do not
make their decision capabilities uniformly linearly close. A supplied
source-norm bound or full matrix access would change the information
contract and is not silently suppressed from a comparison that provides it.

## Focused exact check and failure preservation

[precision_check.py](precision_check.py) failed on its first assertion
because the hand-transcribed numerator used q+2 rather than q+3. The
independent two-by-two inverse exposed that deterministic defect. The
[failure record](precision_failed.json) and executed bytes are preserved;
no hardware cause or cost measurement was invented.

[precision_check_v2.py](precision_check_v2.py) repairs only that numerator
and writes a distinct [result](precision_result_v2.json). Four constructed
R values, 8,32,128,512, pass exact rational inequalities and the unchanged
s16 checker. B returns `below` at the midpoint threshold, while A cannot
return `below` and its upper certificate contains W1. Runtime was 1,554,400
ns, including these four certificate pairs, not a comparison of algorithms.

At R=512, delta is about 3.814668e-6 and the explicit separation about
0.001951203. The ratio is about 511.50. These are sensitivity quantities;
they are neither relative uncertainty-width reductions nor saved CPU work.
The uniform statement comes from W1--W2, not extrapolation from four rows.
