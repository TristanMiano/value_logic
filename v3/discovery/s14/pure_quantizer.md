# Short private episodes cannot always produce a pure lossy summary

Codex (GPT-6), DEVELOPMENT, October 23, 2026 UTC. A distinct information
contract, using ordinary Fourier/decision-tree machinery.

Use the g=2^r-1 Hamming quantizer Q from perfect_code_invoice.md, r>=2.
Call an invoice protocol PURE if its entire public transcript is a function
of Q(x), and the transcript determines Q(x). Thus it leaks no distinction
between worlds in the same one-error cell. This is stronger than merely
achieving the same expected Hamming loss. No earlier loss-only claim is
silently replaced by this purity requirement.

Any such protocol, even with arbitrarily many adaptive private-reset
episodes, requires cap

    H >= 2^(r-1)+2.                                      (1)

The explicit codeword readout has cap g+2^(g-r)-1, so (1) is a necessary
condition, not a matching optimal construction.

## Degree of a function constant on the quantizer cells

Let D be the r-dimensional dual/simplex code, consisting of all parity-check
row combinations. Every nonzero element of D has weight h=2^(r-1).
Characters on the code C are indexed by cosets w+D. Pull the character
chi_w(c)=(-1)^(w*c) back through Q. Its Fourier support lies in w+D, and
its coefficient at v in w+D is

    1 - 2*|v|/(g+1) = 1-|v|/h.                         (2)

Indeed write x=c+e_j, with c uniform on C and j uniform on{0,...,g}.
Orthogonality on C forces v+w in D, and averaging chi_v(e_j) gives (2).
The trivial character w in D yields the constant function: its nonzero
dual frequencies have weight h and vanish in (2).

Every NONTRIVIAL coset w+D contains a vector of weight at least h+1.
For a uniform d in D, W=|w+d| has mean g/2 and second moment(g^2+g)/4,
because the distinct nonzero parity-check columns make its coordinate bits
pairwise independent. If W<=h always, then

    E[W*(h-W)]=h*g/2-(g^2+g)/4=0.

Nonnegativity forces W in{0,h}. A nontrivial coset cannot contain0, so W
would be constantly h, contradicting its mean h-1/2. This proves the claim.
Its coefficient in (2) is nonzero. Different code characters occupy disjoint
Fourier cosets, so these high-degree terms cannot cancel across characters.
Consequently EVERY nonconstant real function of Q(x) has Fourier degree
at least h+1. This is sharp: a coordinate character's coset has maximum
weight h+1.

## Episode consequence

A cap-H invoice cannot use its last answer to change its own count, so each
count-event indicator has Boolean decision-tree depth at most H-1, hence
Fourier degree at most H-1 (the established s13 finite-reset argument).
If H-1<h+1, a count event that is a function of Q must therefore be constant.
The first episode reveals nothing. Inductively the public source remains
the full cube and every subsequent episode is likewise constant. No almost-
surely terminating exact protocol can reveal Q. Independent randomization
does not help when purity and exactness hold after conditioning on its tape.

For the seven-bit code, no pure summary is possible at cap<=5, regardless
of the number of episodes. A protocol may instead reveal extra distinctions
inside the quantizer cells; that is allowed under the earlier loss-only
contract and is NOT ruled out here. This explains one obstruction to
importing an ordinary full-block lossy encoder into a severely bounded
private-computation interface. It does not settle the cap-three lossy
acquisition optimum or establish a new Fourier lower-bound technique.

## The one-episode construction is optimal under purity

For ONE pure episode, each codeword c has one fixed public count. That count
must be at least g. To see why, follow the private query order on the center
c itself. If it reads fewer than g-1 target coordinates, two unqueried flips
leave the one-error ball, so it cannot certify c. If it reads g-1, choose
an error at any earlier queried target coordinate. On that alternative
world, after seeing the error the algorithm must check every other target
coordinate: one further unseen error would leave the ball. Thus some world
in c's cell requires all g reads. Since the cell's count is fixed by purity,
the same lower count applies to every world in that cell. Additional markers
cannot reduce it.

There are2^k equiprobable codewords and distinct counts must decode them.
Consequently H>=g+2^k-1 and mean queries>=g+(2^k-1)/2. The read-all/pad
construction attains both. This establishes its exact one-episode optimum
under the stronger purity contract, not its optimality for all lossy tasks.

Several episodes can reduce the required cap: at cap g+1, recompute Q
privately and reveal one selected codeword bit through counts g/g+1 in
each of k episodes. This is a simple upper construction with paid repeated
work. The general multi-episode minimum cap lies between h+2 and g+1;
the gap is not closed here.

The cheap pure_probe.py screen passed all dual cosets for g=3,7,15 and
2064 exact Fourier coefficients for g=3,7. Exact decision-tree depths of
the16 code characters at g=7 are0 for the constant,6 for seven nonconstant
even-parity representatives, and7 for eight odd representatives. Fourier
degree alone is therefore not the exact decision-depth answer. This screen
does not enumerate nonlinear functions of the codeword or settle the
multi-episode cap. Ordinary Fourier and decision-tree implementations tie.
