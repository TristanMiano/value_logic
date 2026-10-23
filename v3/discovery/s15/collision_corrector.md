# Calibrate residual agreement, then cancel a model's common error

Codex (GPT-6), October23,2026. DEVELOPMENT. Classical self-correction is
the starting point; novelty and useful complete economics are unassessed.

## A fixed algebraic source and a fallible model

Let G,H be finite abelian groups. Independently warranted structure says
the true mathematical function f:G->H is a homomorphism. Let g:G->H be a
fixed cheap model, frozen before calibration. No correctness, homomorphism
or probabilistic-truth assumption is imposed on g. Its residual is

    e(z)=g(z)-f(z).

For independent uniform U,V in G, define the residual collision rate

    beta=P[e(U)=e(V)] = sum_h P[e(U)=h]^2.

One comparison to the true source evaluates this collision:

    e(U)=e(V) iff g(U)-g(V)=f(U-V).                    (1)

Thus two cheap model calls and one exact source evaluation can acquire a
calibration label without computing either individual residual. Sound
positive certificates of (1) can replace full evaluations; unresolved
cases remain unknown rather than being labelled correct.

## Sharp collision-only lower bound for a translated answer

For any fixed target x in G, draw uniform R and propose

    g(x+R)-g(R) = f(x)+e(x+R)-e(R).                  (2)

Write a=max_h P[e(U)=h]. If beta>1/2 then a>=beta>1/2 and

    beta <= a^2+(1-a)^2,
    a >= (1+sqrt(2*beta-1))/2.

The first inequality groups all nonmaximal atoms together; the second
uses the increasing branch a>=1/2. Both R and x+R are uniform, so a union
bound gives probability at least2a-1 that their residuals equal the same
maximal atom. Consequently EVERY x obeys

    P_R[(2)=f(x)] >= sqrt(2*beta-1).                 (3)

This lower bound can be sharp. In an even group with an order-two shift x,
give a subset B of fraction b<=1/2 a nonzero residual h and every other
point residual0. Choose B disjoint from x+B. Then beta=(1-b)^2+b^2,
and equality in (2) holds on exactly1-2b of G, giving equality in (3).
Rational b can be realized in suitable finite groups. This is sharpness
over the class, not a claim that each fixed group admits every fraction.

Therefore beta>5/8 is enough to make each target's correct answer have
probability strictly greater than1/2. For odd k independent repetitions,
returning a most frequent answer has error at most the binomial lower
tail P[Bin(k,p)<=floor(k/2)], where p=sqrt(2*beta-1). The simpler
exp(-2*k*(p-1/2)^2) bound is conservative. Fresh independent shifts are
required for each later adaptive target unless an additional reuse argument
is supplied. The checker-retirement lemma does not apply to unchecked
corrector outputs.

## Partial calibration is enough, if the latent cohort is fixed

Predeclare N independent pairs (U_i,V_i), and let Z_i be the latent
indicator in (1). A computation scheduler may adaptively acquire sound
lower bits L_i<=Z_i, leaving unresolved cases at0. On the single ordinary
Hoeffding event

    beta >= mean(Z)-sqrt(log(1/alpha)/(2*N)),

which has probability at least1-alpha, every truthful later refinement
simultaneously gives the lower receipt

    beta_lo=max(0,mean(L)-sqrt(log(1/alpha)/(2*N))).    (4)

Thus beta_lo>5/8 warrants a corrector for EVERY target. The common event
protects the learned parameter statement; it is not a guarantee that all
later randomized answers will be correct. At horizon T, with fresh shifts
and per-answer ceilings delta_j, total failure is bounded by
alpha+sum_(j<=T)delta_j. A countable preassigned summable budget also works.
Data-chosen g or a growing cohort require a separate valid calibration rule.

## Why absolute prediction accuracy can be the wrong target

If g=f+c for a fixed nonzero c, absolute accuracy is zero, beta=1, and
(2) is exact for every R,x. More generally, a dominant but unknown common
error can cancel without ever identifying that error or the whole function.
The source's homomorphism warrant is essential: it supplies the semantics
of the translation and subtraction. It does not make counterfactual
mathematical truth arbitrary. Ordinary self-correction, invariance and
decision contrasts are the relevant ancestors, and an identical ordinary
implementation ties.

## Cheap unfavorable comparison before an implementation

A generic cheap LOW-RANK LINEAR model is not a suitable positive example
for a linear finite-field f. If g-f is a nonzero linear map of rank d,
its residual is uniform on a q^d-element subspace and beta=q^(-d)<=1/2.
It cannot pass the strict5/8 threshold. A nonlinear approximate program or
preexisting evidence service is needed; merely calling a low-rank model
fallible does not supply the required accuracy pattern.

If f's values on a basis can be acquired cheaply and reconstruct all
answers, ordinary exact interpolation is another mandatory strong control.
Any proposed duty must charge g's construction, calibration labels/proofs,
all2k model calls per answer, group operations, randomness and fallbacks.
The current result is a proposed information/correction contract, not an
observed resource benefit or a replacement for known self-testing theory.

The first correction_probe.py execution checks2370 exact group/shift
cases and1242 equalities in (3), plus explicit sharp families of sizes
8,16,32. A model with zero absolute accuracy gives64/64 correct translated
answers in the common-offset example. These finite constructions are
mathematical illustrations, not a learned-model or runtime experiment.
