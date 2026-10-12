# The quotient stopping rule can use an inexact logical anchor

**DEVELOPMENT derivation — ChatGPT (GPT-6 Astra Pro), October 12, 2026 UTC.**

The [exact quotient tariff](quotient_closed_form.md) assumes an admitted exact
auxiliary optimum C. A useful extension needs only an admitted lower L0 and
a checked fixed auxiliary repair of cost U0, provided their gap is at most the
requested tolerance. This separates the amount of logical evidence needed
for tolerance closure from the more expensive duty of exact optimization.

Keep the same homogeneous mandatory/decision source and nonnegative weights.
Let $`L_0\leq C^*\leq U_0`$, with a checked witness attaining U0.
Assume $`0\leq U_0-L_0\leq\tau<H`$. After h high and l low
mandatory observations, the common mandatory total lies in
$`[na+ah,\ na+a(n-l)]`$. Replacement is certified when:

```math
L_0+na+ah\geq p-\tau.
```

After the decision audit chooses the zero-cost member of its exactly-one pair,
combine that member with the checked auxiliary witness. Its excess over the
best repair is at most U0 minus L0; its excess over replacement is at most:

```math
U_0+na+a(n-l)-p.
```

Thus the same two-threshold policy is sufficient with:

```math
R=\left\lceil\frac{p-\tau-L_0-na}{a}\right\rceil,
\qquad
L=n-\left\lfloor\frac{p+\tau-U_0-na}{a}\right\rfloor.
```

When both thresholds are positive, K equals R plus L minus one is at most n.
The two real threshold arguments are ordered because
$`U_0-L_0\leq\tau\leq2\tau`$. The same ceiling/floor argument as
in the exact derivation therefore applies. Immediate replacement costs zero;
immediate repair readiness costs the decision audit; otherwise the complete
observation cap is KA plus D. This is an **upper bound for a checked policy**.
No information-theoretic optimality of that cap is claimed with an inexact
logical bank, and a new logical purchase or better witness can change it.

If the auxiliary gap exceeds tolerance, learning all mandatory costs alone
need not certify this retained repair: its comparison with the best repair
still has too large a logical gap. Replacement might still close on particular
outcomes. A complete mixed audit/proof quote must retain the unresolved repair
branch and pay to improve its logical evidence; it cannot merely reuse the
exact-anchor stopping formula. This makes the proof-versus-observation choice
explicit without requiring a free exact auxiliary optimum.

No acquisition or implementation test is claimed for this extension. Source
product, separability, witness combination and equality premises require the
same paid original-source checks as the exact family. An ordinary controller
gets the same lower, witness and stopping rule in a comparison.
