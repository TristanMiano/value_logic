# A nonlinear lossy summary can beat every affine-posterior protocol

Codex (GPT-6), DEVELOPMENT, October 23, 2026 UTC. Proposed acquisition
separation under the existing exact invoice interface. The majority
quantizer is ordinary source coding, not a new quantization principle.

## First reject an unproductive cap-three search class

In lossy_vector.md's cap-three setting, suppose every terminal posterior
cell, conditional on independent coins, is an affine subspace of F2^n.
Under the fair prior, each coordinate is either fixed or still fair. If
u(W) coordinates vary in a cell W, its optimal Hamming risk is u(W)/2,
and log2|W|=dim(W)<=u(W). Thus a protocol with expected error at most
delta*n has terminal entropy at most2*delta*n, rather than merely
n*h2(delta). Combining this with the cap-three edge/entropy inequality
gives

    E[fee]>=gamma*n*(1-2*delta), gamma=(7+4*f)/6,

for every reset price f>=0. Recovering all bits with probability1-2delta
and otherwise guessing attains this up to O_f(1). Adaptive parity
measurements, coordinate receipts and their affine intersections therefore
cannot improve the high-reset lossy frontier. A gain must use genuinely
nonaffine terminal cells. This strengthens a structural obstruction,
not the unrestricted high-reset lower bound.

## A general-cap affine lower bound

Let H be the private query cap. For ANY protocol with affine terminal
cells and mean Hamming error D, the public transcript has mutual
information at least n-2D with the input. If Q is the mean number of
unit-cost coordinate queries and R the mean number of used episodes,

    Q>=n-2D, R>= (n-2D)/log2(H),
    E[query+reset fee]>=(n-2D)*(1+f/log2(H)).             (1)

For the query inequality, condition on all independent coins and use the
complete private binary decision transcript: its entropy is at most its
mean number of queries, and the public transcript is a function of it.
For the episode inequality use the H-ary public transcript tree, whose
entropy is at most log2(H) times its mean depth. Public stopping decisions
are determined by that history, not an additional private output channel.
Finite-mean termination permits truncation. These are ordinary entropy
bounds; the special ingredient is the affine-cell error relation.

## A concrete nonlinear construction

Choose odd g, H>=g+1, and n divisible by g with n>=H. On each fresh block
of g bits, privately read the block. If its majority is0, stop at count g;
if its majority is1, query one distinct outside marker and stop at g+1.
Ignore the marker answer. The public invoice reveals the majority, and
the public estimate sets all g coordinates equal to it. The two posterior
cells are Hamming half-balls, not affine subspaces when g>=3.

Put

    G_g=E[|Binomial(g,1/2)-g/2|]
       =(g/2)*binom(g-1,(g-1)/2)/2^(g-1).

The expected error per block is D_g=g/2-G_g and its mean query/reset fee
is g+1/2+f. The error is an average over the declared fair source, not
a claim that every world has this same error. The majority itself is
computed exactly. For the same error target, (1) forces every affine-cell
protocol to pay at least

    2*G_g*(1+f/log2(H))

per block, even when it mixes blocks and adapts globally. Hence the majority
construction is strictly cheaper whenever

    2*G_g>log2(H),
    f > [g+1/2-2*G_g]/[2*G_g/log2(H)-1].              (2)

For example g63,H64 satisfies the first inequality. Both sides of (2)
are exact rationals because log2(64)=6. A small exact arithmetic probe
will report the threshold and a stated fee comparison. The separation
is against ALL affine-terminal-cell protocols, not only a weak chosen
prefix code. It does not show superiority over ordinary nonlinear coding:
the identical conventional majority quantizer attains the same fee.

At larger g with H=g+1, G_g grows on the order of sqrt(g), whereas
log2(H) grows logarithmically. At large reset prices the difference can
therefore be substantial. The associated error target approaches1/2;
do not present this asymptotic statement as a high-accuracy result.

Every block pays for its g reads and marker. Internal majority counting,
controller work, storage and coin costs remain outside the inherited
query/reset tariff. No CPU saving or complete-cost benefit is claimed.
The ordinary interpretation is a repetition-code nearest-codeword
quantizer placed behind a causally constrained invoice channel.

Literature correction: the fair linear-encoder distortion obstruction is
classical (Ancheta 1978, located through Wu 2026). The biased affine-fiber
extension is imported in biased_affine_invoice.md. A nearest-codeword
quantizer for a linear reconstruction code need not have affine encoder
fibers; the affine-posterior comparison must not be called a comparison
against all ordinary linear-code quantizers. The early stopping construction
in majority_stopping.md improves the query bill at unchanged error.
