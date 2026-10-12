# S13C: buying contrasts rather than common action values

Codex (GPT-6), October 12, 2026 UTC. DEVELOPMENT, not confirmation.

## Exact two-action value of a nonadaptive batch

Assume pure observations, two fixed terminal utilities, a coherent uniform
independent distribution on unresolved Boolean coordinates, and known prices.
After substituting current observations and combining duplicate Walsh terms,
write the utility contrast as d=y1-y0=c+sum_e a_e*chi_e. Distinct nonempty masks
are required for the following coefficient analysis. For a chosen additional
batch B, conditional averaging removes precisely the masks not contained in B:

    M_B = E[d | revealed B] = c + sum_{e subset B} a_e*chi_e.

Because max(u,v)=(u+v+|u-v|)/2 and conditional expectation preserves the common
sum, the expected value of sample information is exactly

    EVSI(B) = (E|M_B|-|c|)/2.

The decision objective is EVSI(B)-sum_{i in B}q_i. This explicitly cancels
common action values. It uses the optimal posterior action after the batch,
not a claim about a generic fixed-Q certificate-improvement planner.

The triangle inequality gives EVSI(B)<=sum_{e subset B}|a_e|/2. Therefore the
ordinary closure problem with rewards |a_e|/2 provides an upper bound on the
best net batch value. If its optimum is zero, **no nonadaptive batch has
positive expected net decision value under these assumptions**. A positive
closure value is only a lead. Moreover, if |c|>=sum_e|a_e|, every possible
contrast has the same sign and all EVSI is exactly zero. This stronger cheap
screen can avoid unnecessary evaluation even when the closure bound is positive.

## Rank-sensitive evaluation

The joint law of the completed parity characters is uniform on a linear image
over GF(2). Let their masks span rank r. Choose r independent masks, express
each completed mask in that basis, and enumerate only the 2^r equally likely
basis-parity assignments to compute E|M_B| exactly. Ambient bit dimension and
individual parity degree do not by themselves determine this enumeration cost.
A parity of 64 unresolved bits has rank one and two outcomes. The many
primitive computations can still cost 64 acquisitions; compact prediction does
not make those receipts free.

For nonnegative prices, there exists an optimal nonadaptive batch equal to a
union of supports of completed contrast terms. To see this, discard every bit
that belongs to no completed term. Conditional M_B is unchanged and price does
not increase. Hence enumerating at most 2^k unions, where k is the number of
nonzero contrast terms, yields an exact finite planner. This is useful for
sparse k, but not a polynomial-time assertion for arbitrary k. The rank-based
value subroutine and maximum-closure upper bound can screen candidates. No
generic efficient optimization claim follows solely from low ambient dimension.

## Connection to fallible models and versioned evidence

The uniform-independent model is one explicit forecast, not a theorem about
logical unknowns. For general priors, missing-term conditional means need not
vanish and parity-basis outcomes need not be uniform. A generated observation
plan can instead be compiled as a complete value contrast against the current
terminal policy, including its observation charges and any state transitions.
Its expected gain is then a linear query on the versioned source. A checked
positive lower bound can justify that specified plan within the source event;
a high but fallible acquisition forecast alone cannot. Extending the menu after
data requires a valid common source/prior, a new source, or another explicit
selection correction. Model exploration and forecast learning remain open.

The exact finite algebra here is conventional Bayesian value of information
and Boolean Fourier evaluation. The development objective is a paid controller
that proposes compact useful plans while keeping its warrant separate from
its forecast. Meaningful source acquisition and ordinary complete-cost
comparisons remain necessary for P3-POS01.

## Finite development

[contrast_plan.py](contrast_plan.py) implements GF(2) basis coordinates, exact
rank-space expectation, the closure screen, and exhaustive support-union search.
[contrast01.json](contrast01.json) records 60 cases and 1,278 batch comparisons
against explicit-world conditional action selection. Every chosen plan matched
the enumerated optimum. A 64-bit parity needed two forecast outcomes and two
candidate batches; its supplied-tariff expected net gain was 1/4, with 2.584 ms
planning. Seven terms of rank three over 64 bits needed eight distinct unions;
the best plan bought one 20-bit block for net 3/128, with 7.068 ms planning.
Common-value and sign-dominance cases correctly bought nothing. The latter
also demonstrates a positive closure bound (1/16) with zero true VOI.

The low-rank examples establish the stated representation/count savings within
their known uniform model. They do not measure the costs of computing the bits
or of warranting that model, and ordinary sparse Bayesian planning has the same
construction. This is generative evidence for a compact planning component,
not materially supported P3-POS01 or independent confirmation.
