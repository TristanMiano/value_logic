# Four partial receipts: placement with noise charged

Codex (GPT-6), DEVELOPMENT, October 22, 2026. This continues the explicit
Stieltjes certificate in rational_receipts.md, not a new general principle.

The first four nodes1,2,8,16 give residual bound delta1/25 and coefficient
sum bound9/4. At receipt radius0.001 the certified uniform band is0.0461.
Changing only the placement to8/7,5/2,32/5,14 gives

    delta=117/6475, Lambda=12/5,
    width <= delta*(1+delta)+2*epsilon*Lambda.

At epsilon1/1000 this is972507/41925625, about0.023196, a49.6833% reduction
in the *proved band-width guarantee*. Four partial responses are still used.
These are different placements, not repeated measurements of one workload.
No solve-time, audit-fee or complete-cost saving is established. Different
locations can require different acquisition effort.

## Exact rational certificates and a retained failed bound

Write u=t+16/t in[8,17]. The residual product is

    B(t)=(u-A)*(u-C)/[(u+A)*(u+C)],
    A=106/7, C=89/10, S=A+C=1683/70, P=A*C=4717/35.

Let N=u^2-S*u+P and D=u^2+S*u+P. For the stated delta, delta*D-N
is concave and nonnegative at both endpoints, with equality at17.
The quadratic delta*D+N has positive leading coefficient and negative
discriminant -71208970271/51358890625. Thus |B|<=delta on the whole interval.

The initially proposed coefficient bound Lambda2 is false. At t1 the exact
sum of absolute cardinal weights is1472438/615125, about2.39372. The first
probe stopped on a negative Bernstein coefficient near t1; it is preserved
unchanged. The revised bound12/5 has five exact rational Bernstein
subinterval certificates covering[1,16], stored in receipt_design_probe_v2.json.
The same run passed861 exact kernel identities and2460 finite-law interval
checks. Those finite examples supplement, rather than replace, the uniform
polynomial certificate and the general kernel identity.

The revised coefficient bound is slightly larger than the original9/4.
The new proved width is smaller only when

    epsilon < (26/625 - delta*(1+delta))/(3/10).

The given radius0.001 satisfies this. No claim that the design wins at every
noise level follows. A noise-aware minimax design is a separate problem.

## Analytic optimum within a reciprocal four-node class

For reciprocal pairs t_i*t_(5-i)=16, parameterize the product by

    R_(s,p)(u)=(u^2-s*u+p)/(u^2+s*u+p), u in[8,17].

Equal positive endpoint values require p=136. The unique negative interior
extremum is at u=sqrt(136). Equating its magnitude with the endpoint value
then gives s=10*34^(1/4), and

    delta_*=(25-s)/(25+s) approximately0.01734856.

The corresponding four nodes are approximately1.137803,2.470221,6.477154,
14.062186. They lie in[1,16] and have positive pair sums A,C, where A+C=s
and A*C=136. This product alternates +delta_*,-delta_*,+delta_* at
u8,sqrt(136),17.

For another admissible pair(s',p'), the numerator of R_(s,p)-R_(s',p')
after multiplying positive denominators is

    2*u*((s'-s)*u^2+s'*p-s*p').

Unless the products are identical, this has at most one positive zero.
A strict improvement at all three alternation points would force at least
two positive zeros. Therefore no competitor in this reciprocal class has
smaller uniform residual. This is an elementary restricted alternation
argument, not a claim of a new global Zolotarev result or a noisy optimum.

Ordinary rational interpolation has exactly the same certificate and gains.
Closest-prior placement theory, joint moment envelopes and full acquisition
costs must be compared before calling this a useful original contribution.
