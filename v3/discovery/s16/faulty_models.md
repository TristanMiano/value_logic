# Validating a fault-tolerant registry of model measurements

Codex (GPT-6), October 23, 2026. DEVELOPMENT; constructive synthesis lead.
Error-correcting codes, algorithm-based fault tolerance and randomized
identity checking are direct conventional comparators. No generic novelty
or full-cost gain is asserted.

Let the expensive truth A(x) lie in K^n. Registered cheap models g_j(x)
predict linear measurements L_j A(x), possibly vector-valued blocks.
Assume every coordinate of F_j(x)=L_j A(x)-g_j(x) is a polynomial of
degree at most D over a field. The finite registry, linear maps and degree
warrant are fixed before the validation samples. Allow b faulty model
blocks, rather than assuming all models satisfy their declared relation.

## One test of the registry's global fault budget

At each of k fresh independent points from S^p, |S|=q>(b+1)D, obtain the
full exact A(x), evaluate all models, and accept that point only when at
most b blocks disagree. Accept the registry only if all k points pass.

If more than b residual-vector polynomials F_j are nonzero, choose b+1
such indices and one nonzero coordinate polynomial from each. Their product
is nonzero, of degree at most(b+1)D. Passing one point implies at least one
of those selected coordinates vanishes, hence that product vanishes. Thus

    P(accept a registry with more than b globally faulty blocks)
        <=[(b+1)D/q]^k.                                 (1)

There is no binomial(J,b+1) multiplier: conditional on the fixed registry,
one fixed nonzero product witnesses its invalidity. The test still evaluates
ALL models at ALL validation points and uses the full truth vector each
time. Selection/refitting after failure needs fresh valid accounting; no
unlimited retries against the same samples are granted.

On the common acceptance event, at most b model relations are non-identities.
Therefore at every future input, including adaptive inputs, at most b
measurement blocks can be wrong. The potentially faulty block set is fixed
globally, although a non-identity may happen to evaluate correctly at some
inputs. The proof uses exact polynomial identities, not small numerical
residuals or empirical average accuracy.

## Reconstruction is ordinary block error correction

Define the measurement code C(y)=(L_1 y,...,L_J y). Suppose its block
distance satisfies

    #{j:L_j h !=0} >=2b+1  for every nonzero h in K^n.   (2)

Then the vector of model outputs has at most one y agreeing with all but
b blocks. If two y,y' both fit, their codewords differ in at most2b blocks,
contradicting (2). The true A(x) is that unique y on the common event.

A finite decoder can enumerate presumed faulty subsets of size b, solve
the remaining linear equations and check every residual block. Condition
(2) guarantees that the remaining equations identify at most one y.
The enumeration may be expensive; do not call it a cheap general decoder.
For scalar Vandermonde measurements at J distinct field points, the usual
degree-(n-1) polynomial evaluation code has distance J-n+1, so J>=n+2b
suffices and standard Reed-Solomon decoding is the stronger ordinary control.

This extends the all-valid intersection construction to a different duty.
Blindly intersecting every model equation is now wrong: an invalid model can
make the intersection empty or exclude truth. Conversely, mere majority
agreement cannot replace the distance condition or the paid truth validation.

## A precise component-price screen

Let c_A buy one full truth vector, c_G buy all registered predictions, and
c_D be the per-case decoder/checking cost. Ignoring any unmeasured setup is
not allowed; denote it by c_setup. The startup price is

    k*(c_A+c_G)+c_setup,

and the future-case price is c_G+c_D. A saving against direct truth requires
c_G+c_D<c_A and enough future cases to repay the startup. This is a price
condition, not an observed saving. A control with direct symbolic access to
the true polynomial, cached coefficients or cheaper batch evaluation may
dominate the entire service and must be allowed those resources fairly.

The potentially useful synthesis is one common paid validation event for a
heterogeneous registry followed by deterministic fault-tolerant reuse. Its
statistical rate, coding ingredients and likely fault-tolerance ancestry
need comparison before treating this as a positive contribution. There is
no claim of learning arbitrary mathematical truth or of numerical stability
over floating real-valued model predictions.
