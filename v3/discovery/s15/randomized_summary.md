# Averaged privacy permits a smaller-cap noisy invoice

Codex (GPT-6), October23,2026. DEVELOPMENT; generation pass12.
This changes the disclosure contract explicitly. It does not refute s14's
per-coin pure exact-decoding result.

## Fixed source and observations

Use the classical binary [7,4,3] Hamming code C=ker(A), whose seven parity-
check columns are the nonzero triples. Each raw x has a unique representation
x=c+e, c in C and e either0 or a unit vector. Let Q(x)=c. An episode privately
queries distinct raw coordinates, with cap H; the only public output is its
query count. Private query values and coins are discarded at reset. Padding
queries have ignored answers. Internal arithmetic remains unpriced.

Here purity means the DISTRIBUTION of the public count depends only on Q(x).
It need not hold for each fixed private coin tape. The private tape and timing
are not disclosed. This is a strictly different contract from s14/pure_cap7.md.

For any function phi:C->R let F(x)=phi(Q(x)). Fourier coefficients on the
seven-bit cube satisfy

    Fhat(S)=ahat([S]) * (1-|S|/4),                      (1)

where ahat([S])=E_c[phi(c)*(-1)^(S dot c)] and [S] is the character modulo
the dual simplex code Cperp. This follows directly by averaging independent
uniform c,e. It is a function identity, so it does not require a uniform
deployment source for the channel claim below.

The16 dual cosets have these maximal nonzero degrees in(1): the constant
coset degree0; seven single-coordinate cosets degree5; seven nonconstant
even cosets degree6; the all-ones coset degree7. The dual code's nonzero
words have weight4, where the multiplier vanishes. Thus every pure real
function of degree<=4 is constant.

## No information at cap<=5 in one episode

For each fixed private tape, the event of stopping at h<H is a decision-tree
function of depth at most h. Its multilinear degree is at most H-1. The event
of reaching H is the complement of the other stopping events and has the
same degree bound. Averaging tapes preserves this finite-dimensional span.
At H<=5 a pure count probability therefore has degree<=4 and is constant.
The entire count is independent of c: no nontrivial pure information.

This extends across episodes with fresh independent private tapes and no
retained private state, when the conditional count law at each public history
obeys this purity contract. It does NOT cover correlations hidden across
resets or a weaker condition imposed only on the final transcript.

## A cap6 construction

Choose a code coordinate i. Its lifted sign F_i(x)=(-1)^Q(x)_i has eight
Fourier terms in the coset {i}+Cperp: one weight1 coefficient3/4, four
weight3 coefficients1/4, and three weight5 coefficients-1/4. The sum of
absolute coefficients is5/2. Privately choose one term with probability
proportional to its absolute coefficient, query its support, and return
the sign of that coefficient times the observed parity. Pad to count5
for output+1 or count6 for output-1, using distinct ignored coordinates.

The returned sign Z obeys, pointwise for every raw input,

    E[Z|x]=(2/5)*F_i(x),
    P[Z=F_i(x)|x]=7/10.                                (2)

Thus the public count depends only on the selected code bit, and reveals
nonzero pure information at cap6. Both counts have positive probability;
this construction does not give zero-error exact finite decoding.

Fresh independent episodes can amplify the bit by majority. Four information
coordinates determine c; k odd repetitions per coordinate give codeword-error
upper4*P[Bin(k,7/10)<=k/2]. This is a capability at a smaller permitted cap,
not a fee improvement:4k reset fees can be very expensive. A cap7 exact
construction remains preferable when its interface is available.

## Comparison target and early screen

Randomized decision trees, probabilistic polynomial representations and
randomized encodings are close prior. The code and Fourier identity are
classical. The possible contribution is the precise distinction between
per-tape and averaged disclosure in this paid-invoice interface, with a
sharp cap for any one-episode information. An identical ordinary randomized
encoder ties. The exact screen passed896 input/channel equalities, including
all128 inputs and seven coordinate channels. Four information coordinates
with45 repetitions each (180 episodes) give codeword-error upper below1%.
The primary comparison is recorded in literature.md.

The summary_probe.json limitations string says "No exact finite decoder at
cap6". Read this as a limitation of the constructed channel, as stated above,
not a proved impossibility for every cap6 protocol. Its numerical evidence
and source are preserved; no general zero-error impossibility was checked.
