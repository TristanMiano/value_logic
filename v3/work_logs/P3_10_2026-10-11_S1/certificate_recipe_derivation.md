# P3-10 source-derived certificate semantics

Contributor: **ChatGPT (GPT-6 Astra Pro), principal /root**, 2026-10-11.
Classification: **D/R; independent semantic reconstruction before private outcomes**.
This note states consequences of the unchanged prospective recipes. Observed
delivery and paid cost remain separate questions for the sealed final results.

## Why the loss law simplifies

The `majority_dnf_cnf` recipe compares two expressions for the same Boolean
majority function on each triple of nonzero coordinates. For binary a,b,c,

\[
(a\wedge b)\vee(a\wedge c)\vee(b\wedge c)
 = (a\vee b)\wedge(a\vee c)\wedge(b\vee c).
\]

If at least two coordinates are true, every right-hand pair contains a true
coordinate and one left-hand conjunction is true. If at most one coordinate
is true, no left-hand conjunction is true and the pair of false coordinates
makes the right-hand conjunction false. Conjoining the corresponding triple
expressions preserves equality. The frozen sizes use one or two such triples.

The `selector_mux_sum` recipe compares nested binary selection with a sum of
guarded data bits. The address guards are disjoint and exhaustive: exactly one
guard is true for each address. The arithmetic sum therefore equals the one
selected Boolean data bit, including both possible data-bit values. This
identity holds even though the two public expression trees have different
syntax and one uses admitted rational addition.

Let z be coordinate zero. It occurs in neither identity's address/data/triple
expression. Both recipes therefore have the exact pointwise loss difference

\[
D(w)=2z-1+(left(w)-right(w))=2z-1.
\]

The fourth request adds one half, so its law is `D(w)=2z-1/2`. These are
derivations of the published recipes, not private labels supplied to a paid
worker, a new generator run, or extra final experiment cases.

## The whole incumbent sublevel is the service denominator

The service uses the complete set of hard-feasible states whose rank is no
greater than the supplied incumbent's rank. Its rank has one nonnegative tier.
The active hard edit is `x1 OR x2`. The soft condition prefers `x3=1`, with
weight one until the fourth request and weight two in that request.

| Request | Hard-feasible states, n=4 / n=7 | Minimizers, n=4 / n=7 | Incumbent rank | Required sublevel, n=4 / n=7 | Exact loss range on sublevel | Requested upper bound |
| --- | ---: | ---: | ---: | ---: | --- | ---: |
| 1: initial | 16 / 128 | 16 / 128 | 0 | 16 / 128 | [-1,1] | 1 |
| 2: hard/rank edit | 12 / 96 | 6 / 48 | 0 | 6 / 48 | [-1,1] | 1 |
| 3: nonoptimal incumbent | 12 / 96 | 6 / 48 | 1 | 12 / 96 | [-1,1] | 1 |
| 4: weight/loss/scope edit | 12 / 96 | 6 / 48 | 0 | 6 / 48 | [-1/2,3/2] | 3/2 |

There are 2^n states initially. The hard edit permits three of the four
assignments to x1,x2, leaving `3*2^(n-2)` states. Among those, x3=1 is half,
giving `3*2^(n-3)` minimizers. The normal incumbent has x1=x3=1 and rank zero.
The third request deliberately supplies x3=0 instead, with rank one, so every
hard-feasible state is below or at its cutoff. The fourth request restores the
normal incumbent; changing the soft weight to two changes the worse rank's
value but not the rank-zero set.

Coordinate z is unrestricted in all four current sublevels. Consequently each
listed lower and upper endpoint is attained. For example, set x1=x3=1 and
choose either z value; the remaining coordinates can be zero. A bound over
only one best state would be insufficient. A bound over all minimizing ties
would still be insufficient for request three, which also includes its worse
rank tier. There is no empty-domain or vacuous-bound success in these recipes.

## What the old certificate domains contribute

The two old frames fix z=0 or z=1, respectively, and have no other hard or soft
restriction. Their domains contain 8 or 64 states apiece, according to size.
They are disjoint and their union is the entire Boolean cube. Their exact
loss bounds are -1 and +1.

Every new hard-feasible rank sublevel is a subset of that union. Taking the
maximum of the applicable old bounds therefore gives the current bound one
for the first three requests; the known one-half loss shift gives three halves
for the fourth. This explains why old evidence is relevant to the declared
transport task. It does not make the old inputs, old proof construction,
packet verification, scope checks, or receiving state free. All those paid
steps must remain in the cold/resident invoices and coverage comparison.

The two families test different expression representations with these shared
denotations, under fixed Boolean coordinate semantics. They do not test
discovering an unknown alignment between unrelated ontologies, learning a loss
function, or obtaining an incumbent. Those ingredients are supplied by the
frozen contract.

## Validity, coverage, and usefulness remain distinct

A delivered current certificate may correctly establish the requested positive
upper bound over every required state. That is the B0/B1 service. Because its
upper bound is positive and attained, it does not establish non-deterioration
of the represented loss difference, which would require a nonpositive upper
bound. The request-three incumbent is explicitly nonoptimal. Delivery does
not change the chosen action or optimize that incumbent.

B2 asks a further question: whether a method delivers at least the comparator's
exact current request-ID set, with nonempty service and no more than 95% of its
total cost under the declared tariff. The cost includes all four attempts and
failed deliveries. A lower consumer component can coexist with a larger total;
a cheaper empty response cannot dominate a useful certificate history.

Report n=4 and n=7 separately as well as the declared family aggregates. Do not
relabel sixteen copies of a method's four requests as sixteen independent
semantic task families, or count arithmetic checks of all Boolean assignments
as new experiments. The final schedule still has four streams and 104 paid
histories containing 416 request attempts.

## Independent check and source binding

The defining source is the unchanged `p309_certificates.py`, particularly its
two expression constructors and `_generate_exposed`. It is covered by the
frozen manifest. The certificate reviewer independently evaluates the saved
public expression trees on every Boolean assignment after the final-stage
barrier, and checks these predicted counts, ranks, full loss laws, old-domain
partition, and exact delivered receipts. That check must not import a frozen
generator or reuse a paid proof as its semantic reference.

The reviewer is a separate same-model agent, not a blind or diverse-model
reviewer. Its arithmetic work earns no additional principal research time.
