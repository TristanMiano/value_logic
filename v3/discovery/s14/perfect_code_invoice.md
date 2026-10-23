# A moderate-distortion nonlinear readout using a classical perfect code

Codex (GPT-6), DEVELOPMENT, October 23, 2026 UTC.

The majority examples' error approaches one half. A standard Hamming-code
quantizer gives a smaller-error alternative. The coding construction is
classical; the proposed consequence concerns the inherited paid-observation
interface and its affine-posterior comparison class.

## Exact construction

For r>=2 set g=2^r-1 and k=g-r. Let A be the r by g binary matrix whose
columns are all nonzero r-bit vectors. C=ker(A) has 2^k codewords.
For any x, let s=Ax. If s=0 output c=x; otherwise flip the unique coordinate
whose column is s and output c. Thus x=c+e where e is zero or a unit vector.
The representation is unique: A maps these g+1 errors bijectively to all
syndromes. Uniform x therefore gives independent uniform c and e.

Read all g block coordinates privately. Give each codeword a fixed index
j in {0,...,2^k-1}. Query j further DISTINCT coordinates outside this block,
ignoring their answers, and stop at count g+j. One invoice reveals c. With
cap H=g+2^k-1 and enough ambient padding coordinates,

    Q = g+(2^k-1)/2;
    expected block error D = g/(g+1);
    expected error fraction = 1/(g+1);
    fee = Q+f; one reset per block.                         (1)

Each block also has at most ONE error pathwise. Use disjoint g-bit target
blocks in an ambient n that is a multiple of g and at least H; padding can
query coordinates of other blocks because its answers are ignored. Later
episodes reset private state and pay again. No external output or free
private memory between episodes is assumed.

At the same expected error, every affine-terminal-cell invoice protocol
has fee per block at least

    [g-2g/(g+1)] * [1+f/log2(H)].                          (2)

This includes adaptive affine partitions, not arbitrary ordinary quantizers.
The nearest-codeword encoder here is nonlinear although C is a linear code.
An identical ordinary Hamming quantizer with the same invoice adapter ties.

## Explicit exact seven-bit comparison

r=3 gives g=7,k=4,H=22. The candidate uses14.5 mean queries and one reset,
has12.5% mean bit error, and at most one error in each seven-bit block.
Since22^2<2^9, log2(22)<9/2. Therefore (2) is strictly larger than

    21/4 + 7*f/6.

The candidate fee29/2+f is smaller whenever f>111/2=55.5.
This proves a non-asymptotic class separation without floating logarithms.
The exact-log comparison is stronger. The candidate pays MORE queries;
its benefit comes from fewer reset charges. Computation to form syndromes,
index codewords, decode and control padding is not priced by this tariff.
No complete-computation or CPU advantage is inferred.

## Fallible-model interpretation and limits

After c is observed, the source is uniform on c+{0,e_1,...,e_g}. The complete
model c is false with probability g/(g+1), yet every coordinate prediction
has error1/(g+1), even when that coordinate is selected from c. The affine
hull of this posterior cell is the entire cube: the differences contain
every basis vector. An affine outer approximation therefore discards all
this information. This is a representation limitation, not a limitation
of ordinary probability or code-based reasoning.

For a parity query with support size a, the model parity is wrong with
probability a/(g+1). The Bayes error is min(a,g+1-a)/(g+1), obtained by
flipping the model prediction when a>(g+1)/2. Useful reliance is task
dependent; closure under ordinary model inference would miss this reversal.
The source law, decoder and one-error cell are assumptions/certificates,
not evidence that arbitrary fallible models enjoy the same guarantee.

Classical attribution: Hamming, *Error Detecting and Error Correcting Codes*
(1950), DOI10.1002/j.1538-7305.1950.tb00463.x. Publisher metadata was read;
the Yale PDF and NPS copy were inaccessible in this screen. The elementary
construction above is reconstructed here, not claimed as a new code.

perfect_probe.json passes all32,904 worlds for r=2,3,4 and2,064 small
parity-cell checks. For the seven-bit construction at f=100, the exact
conservative saving is89/1463=6.083390294%; at f=1000 it is
1889/14063=13.432411292%. Evaluating log2(22) numerically strengthens those
comparisons to6.893921825% and14.209370264%, respectively. The exact rational
figures are sufficient for the positive claim. At f=10 the construction
loses. The fifteen-bit version reaches6.25% mean error, but its large cap
and padding bill make it unattractive at the lower reset prices tested.
