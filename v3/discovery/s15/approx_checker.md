# Private residual sketches for fallible approximate answers

Codex (GPT-6), October23,2026. DEVELOPMENT. A constructive continuation
of private_checker.md, with ordinary randomized sketching as prior machinery.
No numerical implementation, priority verdict or complete-cost gain yet.

## The lifetime lemma without perfect completeness

Fix a claim truth relation independent of the private seed R. For every
fixed false claim c require P_R[V_R(c)=accept]<=delta. A proposer sees only
accepted claimed values and the accept bit; all its other information and
randomness are independent of R. Retire this seed permanently on the first
rejection. Then P[any false claim is released before retirement]<=delta.

Condition on all seed-independent information and run an imaginary
all-accept interaction. Its first false claim c_star is fixed independently
of R. If the real interaction has not retired earlier, it reaches the
same c_star. A false release requires V_R(c_star)=accept, whose probability
is at most delta. Earlier false rejections of TRUE claims merely shorten
service. If there is no c_star, no false release can occur.

This reasoning avoids conditioning the pointwise soundness guarantee on
past acceptance. Conditional error after release can be much larger than
delta. There is also no guarantee against later requests if the service
continues with this seed after a rejection or leaks sketch-dependent data.

## Approximate real matrix-vector products

Let A be a fixed n-by-m real matrix and privately sample a k-by-n matrix
R of independent standard normal entries. Precompute G=R*A exactly in
the mathematical model. For a request (x,b,tau), tau>0, the desired
statement is

    ||b-A*x||_2 <= tau.

Let c_delta be the lower delta quantile of chi-square_k. Accept precisely
when

    ||R*b-G*x||_2^2 <= c_delta*tau^2.                  (1)

For each fixed residual d!=0, ||R*d||^2/||d||^2 has this chi-square law.
If ||d||>tau, (1) therefore has probability strictly less than delta.
The lifetime lemma applies even to adaptively chosen x,b,tau, subject to
the private-observation/retirement contract. It bounds every released
approximation in an arbitrarily long epoch by one unconditional delta.

Exact answers always pass. Answers near the tolerance boundary often
cause retirement: at ||d||=tau, acceptance probability is delta. The
checker is useful only if typical proposed errors are substantially below
the permitted tolerance, or if a different verified guard band supplies
availability. The guarantee buys correctness, not a long expected epoch.

A related exact-rational implementation could use independent Rademacher
rows and a proved lower-tail bound with a conservative threshold. This
would avoid ideal Gaussian sampling and transcendental quantiles, but its
dimension/error constants must be reconstructed before use. Ordinary
floating residuals are not exact certificates; rounding and preprocessing
errors need explicit one-sided allowances.

## Availability and model geometry are separate claims

If a fixed cheap model B produces b=B*x, its residuals lie in image(B-A).
A low-dimensional residual subspace permits an ordinary subspace-embedding
bound controlling all its sketch norms simultaneously. Such a bound could
establish that a specified interior tolerance margin prevents premature
retirement for all model inputs. This is a possible availability analysis,
not required for the lifetime soundness proof and not established by a
few passing requests. The source/model/subspace premises have their own
acquisition costs; they cannot be asserted from the private sketch alone.

Preprocessing requires k transposed products with A and storage of R,G.
Each verification requires products R*b and G*x, O(k(n+m)) arithmetic.
The complete bill also includes producing b, generating randomness,
acquiring inputs, fallback after rejection and any refreshed epoch. A
low-rank B can make proposals cheap; an exact full-product proposer would
remove the intended aggregate-work advantage.

The closest comparisons include ordinary residual sketching, adaptive
linear-sketch robustness, private verifiable computation, and deterministic
norm/error certificates. The potentially useful delta is a precise
fail-stop lifetime contract for approximate model use, with complete costs
and availability kept separate. Novelty remains unassessed.

## A conservative checker using only signs and rational arithmetic

Let each row r_i have independent uniform signs in {-1,+1}, and let
G=R*A be acquired exactly. Accept if, for EVERY row,

    4*(r_i^T*b-g_i^T*x)^2 <= tau^2.                  (2)

For a fixed residual d, put mu=||d||_2^2 and Z=r_i^T*d. Expansion gives

    E[Z^2]=mu,
    E[Z^4]=3*mu^2-2*sum_j d_j^4 <= 3*mu^2.

For theta in (0,1),
E[Z^2*1{Z^2>theta*mu}] >= (1-theta)*mu. Cauchy--Schwarz then gives
P[Z^2>theta*mu] >= (1-theta)^2/3. If mu>tau^2 and theta=1/4,
acceptance in (2) requires Z^2<mu/4, hence has probability at most13/16
per row. Independent rows give pointwise false-accept ceiling

    delta_k=(13/16)^k.

Thus23 rows give a lifetime ceiling below1% under the same retirement
contract. This conservative fourth-moment argument is ordinary probability;
it is not asserted to give the optimal dimension or constants. Rational
A,x,b,tau permit exact implementation of (2), including preprocessing.
Integer bit growth and random-bit acquisition are additional costs.

One deterministic availability condition is ||d||_1<=tau/2: then every
row passes. This condition may be unknown to the controller; if a cheap
sound certificate already establishes it, that certificate is a strong
alternative and the randomized checker may be unnecessary. More useful
availability analyses should exploit actual residual geometry and count
the cost of acquiring that geometry.

## An action warrant can ignore arbitrary common prediction bias

Suppose f=A*x is a vector of n action losses and b is a cheap proposed
loss vector. Let P=I-11^T/n, the ordinary orthogonal centering projector.
Use the checker for residual d=P*(b-f), with private rows R and stored
G=R*P*A. After acceptance, choose an action minimizing b+c, where c is
any separately known action-cost vector. Then on the protected event,

    (f+c)[chosen] - min_j (f+c)[j] <= sqrt(2)*tau.      (3)

Indeed, if j minimizes f+c, optimality under b+c implies regret at most
(b-f)[j]-(b-f)[chosen]=(e_j-e_chosen)^T*d, bounded by sqrt(2)||d||_2.
This holds for every c and every tie-breaking choice. Subsequent adaptive
changes of c need no additional model check while x,b and the accepted
norm warrant remain fixed. New x,b,tau may be checked under the lifetime
contract. Acquiring c, choosing the action and the original proposal are paid.

An arbitrary common bias b-f=h*1 is harmless: the contrast residual is
zero, however large h is. Therefore this service tests decision usefulness
rather than full predictive accuracy. Centering and regret duality are
established ordinary mechanisms. An identical conventional checker ties;
the candidate synthesis is the explicit adaptive lifetime/reuse contract
with a resource account, not exclusive ownership of decision-focused ideas.

For exact arithmetic one can avoid irrational sqrt(2) in a declared
regret budget eta by using tau^2=eta^2/2 directly in (2). Centering only
introduces the rational denominator n. Preprocessing, bit growth, privacy
of R,G, model-generation costs and fallbacks still require an actual paid
application before a material benefit can be claimed.

The first checker_probe.py execution passes358 exact moment identities,
718 small-ball cases, and12 adaptive epoch fixtures with256 private seeds
each. It verifies508 accepted true action warrants, the common-bias
invariance and both finite boundary examples. The largest one-row false-
accept probability in that panel is5/8, below the conservative13/16 bound.
This is not a population experiment or evidence of measured speedup.
The23-row ceiling is approximately0.00843; the exact fraction is stored.
