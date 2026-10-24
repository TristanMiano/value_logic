# Sharpness needs an explicit input-column contract

Codex (GPT-6), October 24, 2026 UTC. DEVELOPMENT; pass 25.
This refines the matching-source scope, not the validity of the matrix bounds.

## Finite boundary witnesses need only one extra output direction

Let 0<C<=I, H=I-C, ||c||=1, s=c^T Cc, m0=c^T C^2c and
Q=s-m0>0. For any m in [m0,s), set tau=(m-m0)/Q and

    b=sqrt(tau/Q)*C H c,
    d=1-b^T H^dagger b,
    S=[[C,b],[b^T,d]].                                  (1)

Here b is in range(H). The Schur complement of C in S equals 1-tau>0,
because C^-1+H^dagger acts as (CH)^dagger on that range. Hence S>0.
The Schur complement of H in I-S vanishes, so I-S>=0 and

    rank(I-S)=rank(H)=r.

For v=(c,0), v^T S^2 v=m0+(b^T c)^2=m. Thus S=(I+MM^T)^-1
has a realization M with k+1 rows and only r columns. This replaces the
earlier 2k-dimensional dilation in the finite cap-boundary constructions.
At tau=0 a spare output row can be omitted. Directions with C-eigenvalue1
remain untouched. Since rank(I-C)<=rank(M) for every compatible source,
the number r of columns is minimal.

Interior and upper-cancellation matching sources also use r columns.
The lower parameter-infinity case is different: its earlier construction
uses a unit right vector with a prescribed image under M and may need a
right-kernel direction. An additional zero input column supplies it.
Consequently r+1 columns suffice for all the existing constructions;
this is a sufficient uniform bound, not a claim that every case needs it.

## An exact obstruction: one versus two columns

Take C=diag(1,1/2), v=e_1, W the first two coordinate vectors, e=1.
The dimension-unrestricted lower envelope is 1/(1+e^2)=1/2.
But with exactly one input column the sharp minimum is

    (sqrt(5)-1)/2 = approximately .618034.                (2)

Proof, including arbitrary additional output dimensions: write M as a
single column m. C_11=1 forces m_1=0. C_22=1/2 implies
m_2^2=(1+||m||^2)/2, and therefore k=||m||^2>=1. Decompose
the edit d=a v+b m/||m||+z with z perpendicular to both. The objective is

    F(m+d;v)=1-a^2/[1+a^2+(sqrt(k)+b)^2+||z||^2].

At the minimum z=0 and a^2=1-b^2, with -1<=b<=1. Because
sqrt(k)+b>=0, increasing k cannot improve this minimum. Thus k=1 is
optimal, and maximizing (1-b^2)/(3+2b) gives
b=(-3+sqrt(5))/2. Substitution proves (2) and supplies a finite attainer.

With two columns use M=[[0,0],[1,0]] and edit Delta=[[0,1],[0,0]].
The same old C is retained, ||Delta||=1, and the new inverse is I/2.
Thus the missing column changes a sharp endpoint, not just its attainment.
The certificate remains correct with one column; it is then conservative.

## The previous mixed-target example also separates

For the same C and e but v=(3,1)/sqrt(10), the unrestricted lower .45
has the earlier two-column attainer. A single column, in any output
dimension, always gives F>=23/50=.46. To check this exactly, put
beta=27/50, lambda=5/8 and Q=beta I-vv^T. With m_1=0 and
m_2^2=a^2>=1, the Schur complement certifying

    beta*(1+||m+d||^2)-(v^T(m+d))^2 >=0, ||d||<=1,

is that of the positive quadratic matrix Q+lambda I. It equals

    (5785/15378)*(a^2-1)+2287/1537800 >0.

Indeed m's squared component along v is a^2/10 and its perpendicular
component is 19a^2/10-1, so this expression follows by diagonalizing Q
into eigenvalues -23/50 and 27/50. This is an exact rational certificate.
The [small probe](rank_probe.py) sampled45 compatible scalar geometries,
finding a smallest value about.460560346 at a=1, and checked9 rank-minimal
dilations. Those numerical samples do not prove that finer sharp endpoint;
the exact .46 separation and (2) do not depend on their optimization.

This qualification must accompany any sharp-envelope claim. It is a
same-model mathematical refinement of the information/resource contract,
not evidence that the ordinary comparator differs or a generic new
trust-region method has been invented.
