# Proposed coherent-center proof at stop — UNAUDITED

**Status:** proposed proof only; not independently audited or accepted. The main review should continue to call the universal coherent-center claim unresolved pending audit. This file preserves only arguments obtained before the stop instruction; no further exploration, finite search, or experiment was performed by these proof reviewers. Principal clock credit: **zero**.

**Prepared:** October 5, 2026, ChatGPT (GPT-6 Astra Pro), coherent-center lemma reviewer, with a nested proof reviewer. The lower comparison below was reported by the nested reviewer immediately before the stop instruction. Its algebra and case coverage require independent checking.

## 1. Claim and proposed center

Let k >= 2, M >= 0, b = k + M, and

\[
g_h=\frac{k+1}{k-h+1}\quad(0\le h<k),\qquad g_k=b,
\qquad f_r(h)=\frac{\binom hr}{\binom kr},\quad 1\le r\le k-1.
\]

For mu in [1,b], let X_mu be the probability laws x on {0,...,k} with E_x g = mu. Define L_r = min_X E f_r, U_r = max_X E f_r and R = (1/2) max_r(U_r-L_r).

The proposed claim is that X_mu contains a law whose coordinate r lies in [U_r-R,L_r+R] for every r.

The function f_1 as a piecewise linear function of g is concave. Thus its minimum is

\[
p=L_1=\frac{\mu-1}{b-1},
\]

attained by q^- = (1-p) delta_0 + p delta_k. Its maximum U_1 is attained by the law q^+ on the two adjacent levels bracketing mu. Put B_r = E_(q^+) f_r. The candidate coherent center is q^* = (q^-+q^+)/2, with coordinate (p+B_r)/2.

It suffices to prove

\[
2U_r\le U_1+B_r,\qquad
2L_r\ge 2p+B_r-U_1. \tag{1}
\]

These bounds would put every coordinate in the interval centered at (p+B_r)/2 with halfwidth (U_1-p)/2. They would also establish U_r-L_r <= U_1-p, so the claimed radius would equal (U_1-p)/2.

All quantities in (1) are affine on every interval between successive g-levels: each coordinate envelope has knots among those levels. It therefore suffices to check the nodes mu=g_j, j<k; endpoints are immediate. Write t=j/k and a=f_r(j) at such a node. The required inequalities become

\[
2U_r(g_j)\le t+a,\qquad
2L_r(g_j)\ge 2p+a-t. \tag{2}
\]

## 2. Proposed upper node proof

### 2.1 Pairs supported strictly below k

For r>=2 put n=r-1 and, for h>=1,

\[
P(h)=\frac{\binom{h-1}{n}}{\binom{k-1}{n}},\qquad
C(h)=(k+1-h)P(h),\qquad
H_r(h)=(k+1-h)f_r(h)=\frac{hC(h)}k.
\]

On support h<k, tilt a law with E g = g_j by y_h=x_h g_h/g_j. Then y is a probability law with E_y h=j, and

\[
E_x f_r=\frac{E_y H_r}{k+1-j}.
\]

The sequence C is unimodal, as follows directly from

\[
\frac{C(h+1)}{C(h)}
=\frac{h(k-h)}{(h-r+1)(k+1-h)}
\]

where the denominator is nonzero. Also H_r has a single convex-to-concave turn, since

\[
\Delta^2 H_r(h)
=\frac{(k+1-r)\binom h{r-2}-(r+1)\binom h{r-1}}{\binom kr}.
\]

**Envelope step requiring audit:** on the discrete support {0,...,k-1}, the upper concave envelope of H_r is the line from 0 to a maximizer h_* of H_r(h)/h=C(h)/k, followed by H_r itself. The unimodality and single curvature change above are the proposed justification, including ties.

The key elementary estimate is

\[
\Delta C(h)
=\frac{(k-h)\binom{h-1}{n-1}-\binom{h-1}{n}}{\binom{k-1}{n}}
\le1.
\]

Indeed (k-h) binom(h-1,n-1) counts n-subsets with n-1 elements in an initial block of size h-1 and one in its complement of size k-h, and is at most binom(k-1,n). Therefore F(h)=k+1-h+C(h) is nonincreasing. If j<=h_*,

\[
F(j)\ge F(h_*)\ge2C(h_*),
\]

the last inequality using P(h_*)<=1. Combining this with the line part of the envelope proves 2U_r(g_j)<=t+a for the interior-supported laws. If j>=h_*, the envelope equals H_r, and the inequality follows from f_r(j)<=f_1(j). The coordinate r=1 is immediate.

### 2.2 Adding the terminal level, M=0

Internally, the f_r-versus-g slopes are

\[
s_{r,h}=\frac{\binom h{r-1}(k-h)(k-h+1)}{(k+1)\binom kr},\quad 0\le h\le k-2,
\]

and have one increase-to-decrease turn. The terminal slope at M=0 is 2r/[k(k-1)].

If r<=k/2, this terminal slope is at most the preceding slope

\[
\frac{6r(k-r)}{k(k-1)(k+1)}.
\]

Moreover f_r(k-1)=(k-r)/k >= 1/2, the value of the endpoint chord at g_(k-1). The proposed conclusion is that adjoining k preserves the interior upper hull at every interior node. **This hull-attachment assertion is another explicit audit point.** The preceding interior bound then applies.

If r>=k/2, C(h) attains its maximum over h<k at h=k-1, and

\[
\max_{0<h<k}\frac{f_r(h)}{g_h-1}
=\frac{2(k-r)}{k(k-1)}\le\frac1{k-1}.
\]

Consequently U_r(g_j)=p=j/[(k-j+1)(k-1)]. In this case 2p<=t+a follows from f_r>=f_(k-1): for j<=k-2, t>=2p because (k-j+1)(k-1)>=3(k-1)>=2k (k>=3); at j=k-1, t+f_(k-1)(j)=1=2p. The case k=2 is immediate.

### 2.3 Extension to M>=0

At a fixed interior node g_j, every two-point law supported on {h,k}, h<=j, has an f_r expectation nonincreasing in M: the weight on k decreases as its g-value rises, and f_r(k)=1>=f_r(h). Interior-supported expectations are unchanged. Two-point laws suffice for coordinate extrema. Thus M=0 is the worst case for the upper node bound.

## 3. Proposed lower node proof

### 3.1 A global affine minorant

The sequence s -> f_s(h), s=0,...,k, is nonincreasing and convex. Using the chord from (0,1) to (r,f_r(h)) for the prefix s=0,...,r-1, and bounding every later f_s(h) by f_r(h), gives

\[
g_h=1+\sum_{s=1}^{k-1}f_s(h)+M\mathbf1_{\{h=k\}}
\le\frac{r+1}{2}+
\left(b-\frac{r+1}{2}\right)f_r(h).
\]

Here the M-term is at most M f_r(h). Consequently

\[
L_r(\mu)\ge
\max\left(0,\frac{2\mu-r-1}{2b-r-1}\right). \tag{3}
\]

At interior nodes mu<= (k+1)/2, the deficiency of the right side of (3) below p=(mu-1)/(b-1) is nonincreasing in b>=k. On the positive branch this deficiency is

\[
\frac{(r-1)(b-\mu)}{(b-1)(2b-r-1)}.
\]

Its derivative has numerator

\[
-2b^2+4\mu b-(r+3)\mu+r+1,
\]

which is nonpositive for b>=2mu-1; the interior-node condition ensures b>=k>=2mu-1. On the zero branch monotonicity is immediate. Thus the remaining comparison may be made at M=0.

### 3.2 Exact comparison reported by nested reviewer — UNAUDITED

Let m=j, s=k-m, n=r-1. The required comparison of (3) with p-(t-a)/2 reduces to

\[
d:=\frac mk-f_r(m)
\ge\frac2{k-1}\min\left(g_m-1,
\frac{n(k-g_m)}{2k-n-2}\right). \tag{4}
\]

The nested reviewer reported the following complete case proof immediately before the stop instruction. This is preserved without additional checking.

- If m<r, the target lower bound p-(t-a)/2 is nonpositive (with trivial endpoint cases handled separately).
- For m>=r, the elementary hypergeometric bound
  \[
  P=\frac{\binom{m-1}n}{\binom{k-1}n}\le\frac{m-n}{k-1}
  \]
  gives
  \[
  d\ge\frac{m(n+s-1)}{k(k-1)}.
  \]
  The nested reviewer's already-obtained justification of the product bound: bound the first n-1 product factors with their s=1 counterparts, whose product telescopes to (k-n)/(k-1), then multiply by the last factor (m-n)/(k-n).
- For s>=3, split at n_0=2m/(s+1). When n>=n_0, this bound proves the first branch of (4) through (n+s-1)(s+1)>=2k. When n<=n_0, the needed inequality is
  \[
  F(n):=m(s+1)(n+s-1)(2k-n-2)-2kn(ks-1)\ge0.
  \]
  F is concave in n. The nested reviewer checked the endpoints n=1 and n=n_0; at the latter,
  \[
  F(n_0)=\frac{2m(ks-1)(s^2-2s-1)}{s+1}\ge0.
  \]
  The clean return of the already-obtained derivation supplies the other endpoint. Substituting k=m+s gives
  \[
  F(1)=2s^2m^2+(2s^3-5s^2-3s+2)m-2s^3+2s.
  \]
  For s>=3 this is reported to increase with m>=2, and at m=2 it equals 2(s-1)(s^2-2)>=0. This algebra remains unaudited along with the other cases.
- For s=2, m=k-2 and 1<=n<=k-3, the exact value is
  \[
  d=\frac{n(2k-n-3)}{k(k-1)}.
  \]
  The threshold is n_0=2(k-2)/3. For n>=n_0, the needed first-branch inequality is
  \[
  3n(2k-n-3)\ge2k(k-2),
  \]
  reported to follow by monotonicity for k>=5. For n<=n_0, the needed second-branch inequality is
  \[
  (2k-n-3)(2k-n-2)\ge\frac{2k(2k-1)}3.
  \]
  At n_0, the left-minus-right difference is 2(2k-1)(k-5)/9>=0. For k=4, only n=1 occurs and the displayed comparison becomes 20>=56/3.
- For s=1, d=n/k, and the second-branch target in (4) is n/(2k-n-2), so the comparison is immediate for n<=k-2.

If these case calculations and the upper hull assertions survive independent audit, (2), then (1), would prove the canonical coherent-center claim for every k>=2, M>=0 and every nonempty X_mu. That conclusion is **proposed, not certified by this note**.

## 4. Stop-state qualifications

No additional search or experiment was run by the proof reviewers. The parent separately reported one already-completed, predeclared finite candidate check; that finite check is not used as a proof here. No shared main report was edited by these reviewers. The root's stop instruction is in force. All further verification belongs to the independent audit, not this stopped proof task.
