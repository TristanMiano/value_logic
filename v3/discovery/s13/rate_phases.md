# Reset prices select every intermediate aggregation regime

Codex (GPT-6), DEVELOPMENT, October21,2026. A consequence of invoice_rate.md's
candidate theorem, sharpening its finite-cap interpretation. No new timing
benchmark or representation-independent computation tariff is claimed.

Write d=H-1-r, z=2^(-d), and the candidate rate for prelude length r as

    beta_r=1+(f+z)/(r+2-2z),       r=0,...,H-2.

For adjacent r and r+1 (so d>=2), comparing their positive denominators gives

    beta_r <= beta_(r+1)
      iff f*(1-2z) <= z*(r+1)
      iff f <= t_r=(r+1)/(2^(H-1-r)-2).

The thresholds t_0,...,t_(H-3) are strictly increasing: their numerators
increase while their positive denominators decrease. Consequently ALL of
the H-1 shapes occur on the lower envelope, with no skipped regimes.
Prelude r minimizes exactly for t_(r-1)<=f<=t_r, using t_(-1)=0 and
t_(H-2)=infinity. At a threshold the two adjacent shapes tie. At H2 there
is just r0 and no finite threshold. The finite-n dynamic selector can still
choose other shapes near the end; this statement concerns the leading rate.

For H5 the switches are1/14,1/3,3/2. For H6 they are1/30,1/7,1/2,2.
Thus the stronger pure-prefix/pure-block control misses genuine intermediate
optimal-rate regimes, rather than merely losing on a chosen numerical example.
The ordinary implementation of the intermediate program remains the method
itself and ties. The threshold rule can locate the rate-optimal r by binary
search, but exact integer/price precision and finite-policy preparation still
cost work; this is not a complete computation-saving claim.

For fixed f>0 and H growing, the minimizing d obeys

    (H-1-d)/(2^(d+1)-2) <= f <= (H-d)/(2^d-2)

when the optimizer is interior, which it eventually is. These inequalities
give d=log2(H/f)+O_f(1), r=H-log2(H)+O_f(1), and

    beta(H,f)=1+f/H+O_f(log(H)/H^2).

To justify the order: the inequalities first imply d=O_f(log H), then
H-d is comparable to H, giving the matching logarithmic lower bound; z is
then O_f(1/H). Substitution into beta_r proves the expansion. The statement
is about the rate function after taking the large-n limit at each fixed H.
It does not remove the explicit finite-n remainder if H grows with n.

At f0, by contrast, r0 is optimal and beta-1=1/(2^H-2), exponentially small
in H. Any fixed positive reset price eventually favors a large parity
prelude with only a logarithmic stopping prefix. This makes the task-relative
information tradeoff explicit: aggregate preservation becomes valuable when
communication/reset events have a price, even though exact individual bits
would be more informative. The general full-vector optimum at positive reset
price remains a separate open question.
