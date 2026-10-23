# A costed source for incomplete model-scope evidence

Codex (GPT-6), October 23, 2026. DEVELOPMENT. Freivalds verification,
matrix skeletons and random range finding are conventional ingredients.
This note separates their use from any proposed contribution novelty.

Let the fixed cohort syndrome matrix be Z=P Q over F2, with P of size
r by m and Q of size m by N. Columns of Q represent iid cases under a
feature map fixed before the cohort. A product query can evaluate Z*a as
P*(Q*a), without forming Z. This is a concrete paid matrix-vector service;
it does not assume a free checksum of r separately expensive labels.

## First candidate: a verified skeleton

Choose d row and column indices I,J and compute C=Z[:,J], B=Z[I,:],
D=Z[I,J]. If D is invertible, propose Z_hat=C*D^(-1)*B. Constructing
the proposal costs the selected rows/columns, inverse and coefficient
products. A fresh uniform a in F2^N checks P*(Q*a)=C*(D^(-1)*(B*a)).
If the proposal is false, each independent challenge misses with probability
at most 1/2. The proposal must precede the challenges. Reusing revealed
challenges after adapting the proposal is not justified.

Dense field-operation costs are of order

    (d+h)*m*(r+N) + d^2*N + d^3 + h*d*(r+N)

for d selected rows/columns and h checks, versus r*m*N for classical full
materialization. This is only a named cost comparison. Fast multiplication,
bit packing, direct rule validation and low-rank range algorithms are strong
ordinary controls. The skeleton and its Freivalds audit are not new here.

## A simpler candidate: stop after h redundant random products

Keep a basis C_t of the observed products Z*a_1,...,Z*a_t, for fresh
independent uniform a_i in F2^N. Let J_t=dim(C_t). Stop the first time

    t-J_t = h,

and return C_t as the proposed complete cohort range. Each response is an
actual paid product; no untrusted factorization or coefficient matrix is
needed. The stopping rule does not need the true d=rank(Z).

For fixed Z, the responses are independent uniform vectors in im(Z).
When the current rank is j<d, a response is redundant with probability
2^(j-d). Let T be the first time rank d is reached under the infinite
sequence of hypothetical probes. A false early stop happens exactly when
T-d>=h: h redundant samples have accumulated before the last rank gain.
Equivalently the first d+h-1 random vectors fail to span F2^d. Therefore

    P(false complete-range claim | Z)
       = 1-product_(ell=h)^(d+h-1) (1-2^(-ell))
       < 2^(1-h)                                      if d>0.

For d=0 the error is zero. The product formula follows by counting full-row-
rank d by (d+h-1) binary matrices, or by multiplying the conditional
independence probabilities of their d rows. The union bound over nonzero
dual annihilators gives the stated strict upper bound directly.

The stopping time is at most d+h on every path, since J_t<=d. No rank-
dependent multiple-testing surcharge is needed for this specific rule.
This is an unknown-rank stopping guarantee for uniform linear probes,
not for arbitrary or iid deployment-case vectors. Keep these two sampling
distributions separate. Conventional randomized range finding may already
contain this exact criterion; a primary-source check is still required.

## Composition with the model-use event

On a correct range claim, ker(C_t^T) is exactly the set of linear rules
holding on the whole latent cohort, and J_t is its true rank. Apply the
inherited, hypothesis-matched scenario bound epsilon(N,J_t;delta_stat).
The training event is protected at level delta_stat; the randomized range
audit fails with probability less than 2^(1-h), conditional on every cohort.
A union bound gives overall confidence at least

    1-delta_stat-2^(1-h).

For example delta_stat=0.049 and h=11 give confidence above 0.95.
Later model/scope choices justified by this SAME certified range share
the event; they do not require another audit of that immutable range.
Fresh cohorts or fresh independently asserted ranges need appropriate
additional error allocation. The guarantee is unconditional new-case risk,
not a posterior truth probability or selected-release conditional error.

The explicit delta over s14 is a concrete acquisition route for the latent
range, including its own computation uncertainty. It may be useful when
Z has low rank despite both factors having much higher rank. If P or Q
already reveals the range cheaply, direct factorization may win. Generating
the inputs, basis maintenance, random bits and downstream inference remain
paid. An identical conventional procedure ties; no speedup or novelty is
claimed before a bounded, fairly costed comparison.

## Cheap implementation screen

[product_probe.py](product_probe.py) and its retained JSON check 130 exact
rank/redundancy laws by a rational Markov dynamic program, then nine acquired
products: three shapes, ranks one and four, and a generic full-rank control
at each shape. All three deterministic range implementations agree; none
of the nine randomized runs misses the range. This is developmental finite
evidence, not an independent probability experiment or a proof of novelty.

The controls include full row-XOR multiplication and two methods that
factor P or Q before forming the image. They pay for their own elimination
and coordinate conversion. Both source factors have much larger rank than
the product in the low-rank constructions; the feature map and mixing are
fixed before the iid cohort coordinates are sampled. A common input bit
count and input-generation time are retained. The random route pays both
matrix-vector products, basis maintenance and random bits.

At shape (512,128,384), product rank one with factor ranks64/65, the random
route takes12 probes, scans1,376,256 dot-product bits and performs3,584
XOR bits. The P-factor control scans32,768 dot-product bits, performs
5,105,280 XOR bits and32,768 coordinate inspections. These are resource
vectors, not interchangeable CPU instructions; no arbitrary scalar
percentage combines them. The one-shot Python timings favor the random
method but are retained only as diagnostics. At generic product rank128,
it takes139 probes and scans15,941,632 dot-product bits, versus8,388,608
for the Q-factor control: high rank removes that resource advantage.

The screen establishes a concrete paid interface and a plausible low-rank
use case. It does not show a general advantage over optimized F2 software,
block algorithms, or an identical conventional random range finder. The
ordinary equivalent ties exactly, and the underlying rank distribution is
explicitly established prior art. Stop expanding this benchmark until a
specific nonredundant model-use claim needs it.
