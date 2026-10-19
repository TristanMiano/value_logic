# A randomized hybrid with explicit coin and episode prices

Codex (GPT-6), s12 DEVELOPMENT. Extends variable_invoices.md with a
constructible finite controller and a stated partial resource bill.

The fixed hidden input may be arbitrary. Let k requested parity coordinates
remain, with unit acquisition fee, cap H, d=H-1, nonempty episode fee f>=0,
and price gamma>=0 per fresh independent fair random choice. Randomness is
procedure randomness; no law of mathematical truth is assumed. The input must
be fixed before these fresh choices. Queries and marker coordinates are distinct
within an episode, and H<=n ensures a marker outside each data block exists.

Allow two episode types, for any 1<=m<=min(k,d):

* **Parity block B_m:** query m target coordinates, compute their parity, and
  query one marker iff that parity XOR one fresh fair bit is one. The public
  invoice and the bit recover the block parity. Expected query cost is m+1/2,
  exactly one random choice is used, and m target coordinates are discharged.
* **Prefix P_m:** use a fresh fair bit for each newly queried target coordinate,
  stopping at the first zero of input XOR bit; after m ones, query a marker.
  An invoice j<=m reveals the first j transformed bits as 1^(j-1)0; invoice
  m+1 reveals m ones. The public random bits recover the corresponding original
  bits, whose parity is accumulated. A random bit is purchased only when used.

The number of prefix random bits consumed is min(invoice,m), so exposing their
consumed prefix introduces no further answer-dependent channel beyond the
invoice. Equivalently they may be made available by a public random tape with
priced accesses. Fees f and gamma are separate from the visible query count;
for these two episode types their actual charges are already determined by the
public action and invoice. General algorithms exploiting a different billing
channel are outside this restricted controller class.

Let U(k) be the minimum expected surcharge above the mandatory k target
queries, counting f and gamma. Set U(0)=0 and mu_m=2*(1-2^(-m)). Then

    B_m = 1/2 + f + gamma + U(k-m),
    P_m = 2^(-m) + f + gamma*mu_m
          + sum_(j=1..m) 2^(-j)*U(k-j) + 2^(-m)*U(k-m),
    U(k) = min_(m=1..min(k,d)) {B_m, P_m}.

The prefix's j-th zero has conditional probability 2^(-j) for every fixed
input and public history, and all m ones has probability 2^(-m). These facts
justify the recurrence without a truth prior. Discarded marker answers do not
change the next state. Optimality here is exactly over the declared hybrid
class; it does not compare every possible private query program.

Direct evaluation uses O(k*H^2) arithmetic; cumulative weighted sums can reduce
this to O(k*H). Exact rational bit complexity, table storage, parity operations,
invoice parsing and physical random-bit generation are additional real costs.
The bill explicitly prices random choices, but is not an all-in wall-time claim.

## What the prices can reverse

For pure prefix recovery on a long stream of target coordinates, let
beta=1/(2^(d+1)-2). Per target coordinate, expected query surcharge tends to
beta, episode count tends to 1/2+beta, and random-choice count is one. Fixed
parity blocks of size d instead have asymptotic surcharge 1/(2d), episode
count 1/d, and random-choice count 1/d. Prefix is cheaper under the declared
bill precisely when

    f*(1/2 + beta - 1/d) + gamma*(1 - 1/d) < 1/(2d) - beta.

For H=3 this becomes f+3*gamma<1/2. For H=4 it becomes
5*f+14*gamma<2. Boundary effects and hybrid choices can change finite-n
decisions; these are comparisons of two pure strategies, not a complete
policy classification. In particular, more private capacity does not make
the reset and controller charges disappear.

The ordinary comparator receives exactly the same randomization and protocol
menu. It therefore realizes the same controller. The potentially useful delta
is the explicit interface construction, its every-input expected-fee guarantee,
and a rule for choosing between modes under priced resources, rather than a
claim to outperform an identical conventional implementation.

## First finite screen and a stronger control found afterward

The unchanged first [hybrid_probe.py](hybrid_probe.py) execution passed 12,096
explicit input/tape executions and 504 every-input conditional-mean checks in
27 small panels, plus 12 exact n=100 DP calculations. It made 9,832 named
candidate evaluations in 0.1365771 seconds. These are finite construction
checks; the DP class is not an unrestricted private-program oracle.

**Comparator correction:** the frozen probe prices one fresh coin per fixed
block. A stronger fixed-block controller can share ONE fair orientation coin
across all predetermined blocks. Each marker is still fair for every fixed
input, so its mean query fee is unchanged while its total coin count falls
from q to one. Therefore gains printed against independently randomized
blocks at gamma>0 are not gains against this stronger control. The zero-coin-
price calculations are unaffected. Preserve the original result and use the
extension in [randomness_price.md](randomness_price.md) for the fair comparison.
