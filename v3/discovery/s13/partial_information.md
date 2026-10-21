# Partial invoice feedback cannot improve the leading Fisher-information price

Codex (GPT-6), DEVELOPMENT, October20,2026. Connects the new invoice charging
lemma to the question left open in s12/information_price.md. The statistical
identities are ordinary likelihood/Fisher-information identities. This is a
proposed consequence of the new channel-specific bound, not a general theorem
that exact answers always beat partial measurements.

## Source and experiment

Let chi(x) be sign parity of all n coordinates and

```math
P_\theta(x)=2^{-n}(1+\theta\chi(x)),\qquad |\theta|<1.
```

Use the same cap H, query/reset fees and private-reset exact-invoice interface
as invoice_rate.md. The public experiment may stop with a partial transcript;
it need not decode parity. Condition on an independent random tape. A terminal
transcript t has compatible cell W_t and uniform-source parity bias
m_t=E_0[chi(X)|t]. Its likelihood is P_theta(t)=P_0(t)(1+theta*m_t).
The Fisher information at theta0 is therefore J=E_0[m_t^2]. Let C be its
expected query-plus-reset fee under P_0, and beta=beta(H,f).

If some independent coins are private, reveal their full tape only for the
lower-bound argument. This can increase E[m^2], by conditional Jensen, while
leaving the actual expected fee unchanged. The bound on the augmented
transcript therefore implies the bound on the actual observed transcript.
The likelihood identity itself holds for any fixed stochastic observation
kernel too, using m_t=E_0[chi(X)|T=t] rather than a literal uniform cell.

## Bound from the same edge potential

Write W_+ and W_- for the two parity classes in a terminal cell W. Every cube
edge crosses these classes, and every vertex has degree n. Thus

```math
E(W)\le n\min(|W_+|,|W_-|)
       =\frac n2 |W|(1-|m_W|).
```

The initial normalized edge potential is n/2. The expected residual is at
most (n/2)(1-E_0|m_t|). The local charging lemma then gives

```math
C\ \ge\ \beta n\,\mathbb E_0|m_t|
   \ \ge\ \beta n\,J.
```

Equivalently, append the best parity guess at each terminal cell and apply
invoice_rate.md's bounded-error result: its error is
(1-E_0|m_t|)/2. Both derivations expose the same dependency. Uninformative
experiments have J0 and do not define a favorable C/J ratio.

An exact parity decoder has J1 and fee at most beta*n+O_(H,f)(1). Consequently
the optimum local information price C/J lies between beta*n and that exact
decoder price. Partial observations cannot improve its leading coefficient as
n grows with H,f fixed. This does not prove finite-n equality: for example the
lower bound and exact decoder still have a nonzero small-n gap. The old72
three-bit screens remain finite evidence; they are not reclassified as proofs.

## A more explicit price of unresolved bias

If every nonzero terminal bias has magnitude at most b<=1, then m^2<=b|m|,
so C/J>=beta*n/b. Producing only weakly biased outputs can therefore be less
efficient than occasionally revealing a complete parity. Randomly buying an
exact answer with probability q and otherwise returning no information has
J=q and C=q*C_exact, retaining the exact experiment's information price when
the independent coin and its public processing are free.

For N fresh independent source instances, experiments may be chosen using
previous public outcomes. At theta0, conditional scores have mean zero and
Fisher information adds across the N experiments. Applying the bound
conditionally gives total expected fee at least beta*n times total Fisher
information. This statement is for a fixed finite N; random stopping requires
additional integrability/optional-stopping justification. It does not charge
the work needed to compute posterior biases or select an experiment.

## Nonlocal identities and boundaries

The same cell likelihood gives the exact identities

```math
\chi^2(P_\theta^T\Vert P_0^T)=\theta^2J,
\qquad
\mathrm{TV}(P_\theta^T,P_{-\theta}^T)
 =|\theta|\,\mathbb E_0|m_t|.
```

Thus the fee bound also limits these single-instance distinguishability
quantities. This is not an unqualified many-sample testing/sample-complexity
claim. Nonuniform nuisance laws, targets other than full parity, correlated
fresh instances, noisy readout and omitted controller prices need their own
analysis. Exact observation of ordinary query answers changes the interface
and removes the invoice coefficient; an ordinary realization of this same
experiment ties it.

partial_probe.py passed360 generated adaptive public protocols, using7259
private programs and3777 terminal cells, over n3–6, caps2/3/n and reset
fees0,1/2,3. It checked the edge, parity-error, whole-vector-error, Fisher and
divergence inequalities with rational arithmetic. 209 protocols had positive
information;191 had information strictly between zero and one. These counts
include random inefficient programs and are not evidence of a useful policy
or broad optimality. The screen took0.1356363 seconds in total.
