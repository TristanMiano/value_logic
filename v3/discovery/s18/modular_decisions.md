# Modular values for a bounded integer decision

Codex (GPT-6), s18 DEVELOPMENT. Chinese remaindering, error-correcting codes,
polynomial fingerprints and modular nonzero certificates are immediate prior.
This is an early information/cost screen, not a new arithmetic algorithm.

An unresolved nonnegative integer X is warranted to lie in{0,...,N}. A paid
query returns X modulo a selected modulus. The action question is X>K for
a fixed integer0<=K<N. Exact modular evaluation, the bound N and query
prices must actually be available; arbitrary mathematical truths do not gain
a cheap modular oracle by this definition.

## Uniform worst-case threshold identification is not easier than recovery

For fixed moduli, the residue vectors form a finite code. Two integers x,y
have equal coordinates exactly at moduli dividing their difference D=|x-y|.
For every D in{1,...,N}, some pair on opposite sides of K has that difference:
take x=max(0,K+1-D), y=x+D. Both are in the domain and x<=K<y.

Thus the minimum Hamming distance across the decision boundary equals the
minimum distance between any two distinct integer codewords. Correction of
up to r arbitrary residue errors uniformly over this full interval therefore
needs the same distance>2r as full integer recovery. With r=0, all cross-
boundary collisions disappear iff every integer is identified. This rejects
a uniform fixed-code advantage based only on asking a binary question.
It does not reject instance-dependent early stopping or other query types.

## One-sided exclusion can nevertheless be inexpensive on particular inputs

For an exact prime residue, if p>K and X mod p>K, then X>K is certified
without reconstructing X. This is ordinary modular non-membership. Suppose
X>K and choose uniformly from q distinct primes, each at least P>=2 with P>K. A prime
that fails this test divides at least one of X,X-1,...,X-K. Hence the number
of failing primes is at most

    (K+1)*log(N)/log(P),

by the product bound on these nonzero integers. The failure probability is
at most beta=min(1,(K+1)log(N)/(q log(P))). Fresh independent prime choices
give beta^t as an upper bound on still lacking this certificate after t tries.
The probability concerns the algorithm's query randomization for EACH fixed
integer X>K; it is not a learned probability that a mathematical statement
is true. No false positive is possible with sound exact residues.

For X<=K this test never certifies the low side. A zero-error decision
procedure must retain an actual low-side proof or complete-recovery fallback;
simply declaring X<=K after unsuccessful trials changes the correctness
contract. Prime-list construction, residue verification, failed attempts and
the fallback are part of the cost. A deterministic stronger lower bound on
X may settle the decision before any modular query, and must be compared.

A natural possible interface is a nonnegative combinatorial count computed
by a determinant modulo primes, such as a spanning-tree count. This is only
an application lead. Direct combinatorial bounds and established adaptive
Chinese-remainder/early-termination methods are mandatory controls before
an implementation or economic claim. Do not use a full-integer computation
as the only baseline.

The initial screen finds an established modular controller with replaceable
stopping rules in Dumas/Gautier/Roch2010. A threshold predicate fits that
interface directly. Keep the elementary decision/recovery boundary and the
one-sided certificate, but park a generic early-termination contribution.
No implementation is justified by this screen alone.
