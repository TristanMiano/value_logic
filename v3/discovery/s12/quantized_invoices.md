# Quantized invoices: visible thresholds determine the parity price

Codex (GPT-6), s12 DEVELOPMENT derivation. Extends the private-reset invoice
interface to a coarser observation, rather than assuming exact real-valued
readout. No all-size independent verification or priority claim yet.

There are n>=2 hidden Boolean coordinates with unit acquisition fees, and
2<=H<=n distinct coordinates may be queried privately in an episode. Its
actual acquisition count is C in {0,...,H}. The only public observation is
Q(C)=floor(C/Delta), for a known positive integer bucket width Delta. The
controller knows when the episode completes; no other timing/answer channel
is available. A nonempty episode additionally costs f>=0, separately billed
and excluded from Q. Quantizing C+f instead would be a different contract.
Private answers are erased at reset; repeated queries in later episodes are
allowed. The requested answer is the parity of a fixed set S, with k=|S|.

Put B=Delta*floor(H/Delta), the last visible positive threshold. If B<=1,
no nonconstant task can be learned: for B=0 every invoice is the same, and
for B=1 the only possible threshold is paid before any answer is available.
The empty parity costs zero. Assume B>=2 and k>0 below.

## One episode has exact observation span through degree B-1

The event C>=b, at a visible threshold b in {Delta,2Delta,...,B}, is determined
before buying the b-th coordinate. It is therefore a Boolean decision tree of
depth at most b-1, with Fourier degree at most b-1. Quantized invoice events
are differences of these threshold events, so every observation likelihood
has degree at most B-1.

Conversely, for any set T of at most B-1 coordinates, query them and pad with
other distinct coordinates to a total of B-1 purchases. Buy one final distinct
marker iff their parity is one. The two public buckets differ. Thus this
experiment recovers the character on T, and the span of obtainable likelihoods
is exactly the space spanned by Boolean characters of degree at most B-1.
This is a finite observation statement; it does not provide the source's law.

## Exact hard-worst acquisition and reset fee

Let q=ceil(k/(B-1)). The optimum zero-error hard-worst invoice is

```math
\boxed{\quad
\Delta\max\left(q,\left\lceil\frac{k+q}{\Delta}\right\rceil\right)+qf.
\quad}
```

**Lower bound.** Follow a public path taking a maximum compatible bucket at
each informative episode. If its visible threshold is b_j, the corresponding
event on the current source equals C>=b_j and has a global degree-(b_j-1)
extension. The product of these extensions is the path indicator: it is
nonzero and supported on one target-parity class. Its target Fourier
coefficient is nonzero, so sum_j(b_j-1)>=k. Every b_j is a positive multiple
of Delta at most B, and the selected path pays at least sum_j b_j plus tf.
Hence t>=q and

    sum_j b_j >= max(t*Delta, Delta*ceil((k+t)/Delta)).

Both this lower bound and tf are nondecreasing in t, so t=q gives the boxed
bound. The argument uses maxima of public buckets, not an unwarranted exact
cost observation. Positive uninformative episodes can be omitted.

**Construction.** Let L=Delta*max(q,ceil((k+q)/Delta)). Choose q thresholds
b_j in {Delta,...,B} summing to L; this is possible because q*Delta<=L<=q*B.
Their total data capacity L-q is at least k. Partition S into q nonempty
blocks T_j of sizes at most b_j-1 (k>=q), using those capacities. In episode
j query T_j, pad with other distinct coordinates to b_j-1 purchases, then
buy one more distinct marker according to its parity. The public side decodes
each block parity from whether the threshold b_j was crossed. Worst total
is L+qf, attained when all block marker conditions hold. There are enough
coordinates for padding because b_j<=B<=H<=n. Padding may redundantly query
another block's coordinates; its answers are discarded.

Randomization cannot improve this zero-error hard-worst bound: as in the exact
invoice theorem, fix a random tape valid on every member of the finite cube.
Expected cost is a separate optimization problem.

## Resolution effects and next screen

For Delta=1, B=H and the price reduces to k+ceil(k/(H-1))*(1+f), recovering
the unit-price exact-invoice formula. At Delta=2,H=3, B=2: the third private
purchase gives no higher observable bucket, so only degree-one information
can be transmitted per episode. Full parity then costs 2n+n*f. At Delta=2,
H=4,k=5 (n>=5), the formula gives 8+2f; the exact-invoice price is 7+2f.
If H<Delta, every episode is observationally constant and resets cannot help.

Prospective finite screen: transform the already frozen full private-program
bank by Q, independently solve the public worst-cost problem while retaining
actual C costs within each bucket, and compare the formula for small n/caps.
Grouping solely by observed bucket must not incorrectly replace the actual
cost by its lower endpoint. The private-program contract and uniform unit
fees are essential to this simple formula; arbitrary quantizers and unequal
prices need a separate analysis.

The unchanged first [quantized_probe.py](quantized_probe.py) execution passed
192 comparisons at n=3, caps two/three, bucket widths one through four, all
target masks and overheads 0,1,3. It used 8,673 residual-budget states and
27,851 private-program choices, explicitly retaining 5,328 encountered
heterogeneous bucket cases across panels. Runtime was 0.2524154 seconds.
The oracle tracks a remaining budget for every compatible world; charging a
bucket's maximum immediately and then adding an independently optimized
continuation could otherwise combine incompatible worst cases. The result is
a finite DEVELOPMENT check, not a general confirmation.

## Arbitrary monotone quantizers: a priced capacity cover

The same proof extends to any fixed nondecreasing Q on {0,...,H}. Let
J={b in {2,...,H}:Q(b)>Q(b-1)} be its useful visible thresholds; a jump at one
alone carries no answer-dependent information. If J is empty, nonconstant
parity cannot be learned. Otherwise the exact price is

```math
F(k)=\min\left\{\sum_j(b_j+f):\ b_j\in J,
                              \sum_j(b_j-1)\ge k\right\},\qquad F(0)=0.
```

Equivalently F(k)=min_(b in J)[b+f+F(max(0,k-(b-1)))]. This is an ordinary
integer capacity-cover recurrence, with O(k*|J|) arithmetic evaluation. The
maximum-bucket path supplies one threshold capacity b_j-1 and pays at least
b_j in each informative episode; the padded parity-block construction attains
any such capacity cover. Dominated zero-capacity jumps are omitted. No claim
is made for nonmonotone encodings of counts.

Unlike equal-width buckets, an arbitrary threshold set can make more episodes
cheaper: J={2,100}, f=0 and k=2 costs four using two threshold-two episodes,
instead of one threshold-100 episode. The general recurrence is preferable
to an unjustified rule of always taking the largest available private block.
This extra generalization has not yet been independently probed.

On a checked affine source x0+V, replace k by the smallest Hamming weight in
the target character's coset modulo V-perp. The earlier affine Fourier
argument gives a representative of weight at most the path's total capacity;
the capacity-cover price is nondecreasing in k, yielding the lower bound.
Recover that representative and apply the known affine offset for the upper
bound. Finding the minimum-weight representative is not generally cheap;
source acquisition, decoding and controller work remain additional costs.

The unchanged first [readout_probe.py](readout_probe.py) execution checks the
generalization on every three-bit affine source, every partition of positive
counts at caps two/three, every target, and overheads 0,1,5. All 7,344 monotone
comparisons pass. Another 1,224 nonmonotone comparisons also agree with the
jump-cover expression, but that observation is exploratory: the maximum-bucket
proof uses monotonicity and has not established the nonmonotone extension.
The run used 21,057 residual-budget states and 43,837 program choices in
0.5683634 seconds. Both probe sources and their outputs are now frozen.
