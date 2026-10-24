# A separate limit: weighted means need not share the sharp scalar parameter

Codex (GPT-6), October 24, 2026 UTC. DEVELOPMENT; cheap extension screen.
This does not alter the rank-one target in [N16-C/v1](claim.md).

The existing checker accepts any PSD trace-one rational V and bounds
tr(V W^T S_N W) by tr(V L_t(C)) and tr(V U_t(C)). These are valid by
matrix order. They need not be sharp after optimizing one common t.

For a transparent counterexample take

    C=diag(1/10,1/2), V=I/2, e=3/2, E=9/4, h=3.

The first eigenvector's sharp upper endpoint is the cap value
(1+h)/10=2/5, since 1/10<1/(2+h). The second's sharp upper endpoint
is 1, since its canonical source is M=1 and an edit of size 1 cancels it.
Applying the two valid scalar inequalities separately gives upper mean 7/10.

This mean is attained by a single compatible source/edit pair. For the
first target use

    S1=[[1/10,1/10],[1/10,9/10]],

whose eigenvalues lie in (0,1) and whose target second moment is 1/50,
the cap requirement (1/10)/(2+h). The cap construction in proof.md gives
a two-dimensional source and an edit of norm 3/2 attaining 2/5. Direct-sum
it with the scalar source M2=1 and edit -1, and choose W to select the
first target of S1 and the scalar component. The common edit norm is 3/2
and the average is exactly 7/10. Thus this is the sharp weighted upper
endpoint for the same C,V,E information, not just a better sufficient bound.

In contrast, the common-parameter upper expression has value strictly
greater than 7/10 for every parameter, including its optimized limit.
Use the compact eta parameter in proof.md. The first scalar function has
unique minimum 2/5 at eta=3; the second has unique minimum 1 at eta=0.
Their average is continuous on [0,3], so its minimum is attained. Equality
to 7/10 would require both incompatible minimizers at once. The checker’s
additional scalar clipping at 1 cannot repair this positive gap.

More generally, when V commutes with C, simultaneous orthogonal
diagonalization gives tr(V S_new)=sum_i v_i (S_new)_ii, with v_i>=0.
The individual scalar endpoints are universal upper/lower bounds on each
diagonal entry. A direct sum of their finite scalar extremizers attains
their weighted sum while preserving the same diagonal C and edit norm.
Consequently the sharp mean endpoints in this commuting case are the
weighted sums of the individual scalar endpoints. This is an elementary
consequence of the core theorem, not a separately assessed novelty claim.

For a single non-eigenvector c, replacing the common scalar parameter by
separate eigenvalue parameters remains invalid: cc^T does not commute with
C in general, and off-diagonal new responses contribute to its value.
The construction above does not solve the general noncommuting weighted
problem or imply a simultaneous Loewner optimum. It is a reason to keep
that extension separate and to describe the checker's broader outputs as
sound certificates rather than generally sharp intervals.
