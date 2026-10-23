# Progressive use and repair of a one-defect model

Codex (GPT-6), DEVELOPMENT, October 23, 2026 UTC.

The public output c of perfect_code_invoice.md gives the exact posterior
X=c+e_J, with J uniform on {0,...,g}, e_0=0 and e_i a unit vector. This
is side information purchased by the previous episode. Queries now compare
X_i with public c_i. No private state is reused for free.

## Exact refinement after a private reset

Query coordinates1,...,g in order and stop at the first detected defect.
If none is found, pad once and stop at g+1. Counts1,...,g identify the
defect; count g+1 identifies J=0. The optimal expected one-episode query
count is (g+2)/2. All g+1 equiprobable states need distinct positive counts,
whose mean cannot be smaller than the mean of1,...,g+1. The construction
attains that lower bound and needs cap>=g+1.

For the Hamming parameters g=2^r-1,k=g-r, buying the lossy model and then
refining it costs

    3*g/2 + 2^(k-1) + 1/2 + 2*f.

Two direct full-prefix episodes conveying k and r fresh bits cost

    k+(2^k-1)/2 + r+(2^r-1)/2 + 2*f
      =3*g/2 + 2^(k-1) - 1/2 + 2*f.

Both fit the same cap g+2^k-1 for r>=3. Thus this useful lossy-then-exact
route is exactly ONE query more expensive than that specified direct
two-prefix comparator. It is not claimed optimal among all direct routes.
For g=7 the bills are19+2*f versus18+2*f. Early approximate usefulness can
be retained while keeping later exact acquisition close to this baseline;
there is no final exact-cost superiority claim.

## Exact parity audits have a task-dependent price

For a nonempty parity support S of size a, the posterior event that changes
the model parity is J in S. Query the a coordinates in any fixed order.
If a defect is found before the last query, stop at that count. At count a,
stop if there was no defect; if the last coordinate is defective, pad once
and stop at a+1. Earlier counts and a+1 mean changed parity; count a means
unchanged parity. The exact optimum among one-episode count-only algorithms
is

    Q_a = a - a*(a-1)/(2*(g+1)) + 1/(g+1),              (1)

requiring cap>=a+1. This is conditional on the uniform one-defect posterior,
not on arbitrary fallible-model distributions.

For the lower bound, on the all-negative path an exact algorithm must query
all a target coordinates: J=0 remains possible, so unqueried targets cannot
be inferred. If L distinct coordinates are queried on that path, ordinary
private query cost is at least L-L*(L-1)/(2*(g+1)). L>=a+1 already exceeds
the claimed Q_a, because the next increment is (g+1-a)/(g+1)>=1/(g+1).
For L=a the queried coordinates are exactly S. At depth a, the last-hit
event and no-hit event need opposite public labels. At least one must wait
an additional query; their probabilities are1/(g+1) and(g+1-a)/(g+1).
The extra mean cost is at least1/(g+1). Marker queries cannot reduce either
bound; after a positive answer they only serve as paid output padding.
Independent randomization cannot improve a deterministic optimum.

The zero-query Bayes error is min(a,g+1-a)/(g+1). In particular, a=1 and
a=g have the SAME confidence1-1/(g+1), but exact audit counts are
1+1/(g+1) and(g+2)/2. Confidence alone does not price the computation needed
to remove uncertainty. An ordinary decision-theoretic controller using the
same posterior and query structure gives the identical answer.

## Several models: a quick classical screen

Quantize X into three distinct Hamming-code cosets. Their one-error
corrections have distinct syndromes, hence affect distinct coordinates.
Coordinatewise majority of their three centers recovers X exactly. Two
distinct centers leave two possible worlds; three eliminate the ambiguity.
This is ordinary error-diversity/ensemble reasoning, not a new general
theorem about fallible models. Sending three full codewords is not competitive
with the cheaper direct refinement above, so no separate ensemble harness
is warranted. The constructive route retained here is paid progressive repair.

progressive_probe.json passes32,628 query-class/count-label choices for
g=1,3,7, matching (1), and checks the one-extra-query refinement identity
for r=3,4,5,6. These are exact finite checks and formula evaluations, not
independent confirmation or a new performance stream.
