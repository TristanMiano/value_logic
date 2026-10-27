# What symmetric binary optimum losses reveal about a probability law

Codex (GPT-6), s19 DEVELOPMENT. A bounded Q5 construction. The exact optimum
value oracle, known losses and common probability law are premises. This is
not a sample estimator or a claim that mathematical truths are random draws.

Let p be a law on d named outcomes. For each singleton event {i}, retain only
the optimal zero-one prediction loss

    r_i = min(p_i,1-p_i),

without the optimal prediction label. These are ordinary binary Bayes risks.
Put s=sum_i r_i. At most one p_i exceeds1/2.

- If s=1, then p_i=r_i for all i, uniquely.
- If 0<s<1, any compatible law has one majority coordinate a with
  r_a=s/2. It is obtained by p_a=1-r_a and p_i=r_i for i!=a.
  Conversely every such a supplies a compatible law.
- If s=0, the compatible laws are exactly all point masses.

For the middle case, two different majority candidates can exist only when
exactly two r coordinates are nonzero and equal. Thus singleton optimum
losses identify every law with at least three positive coordinates. A
nonuniform law on exactly two outcomes remains ambiguous under swapping
its two masses; all point masses remain mutually ambiguous.

In fact no further symmetric binary-event optimum-loss query can resolve
those exceptional classes. For a two-point support, every event has mass
0,1,p or1-p; swapping the masses preserves min(p(A),1-p(A)). For point
masses every such risk is0. Thus the listed ambiguity is exact even if all
binary-event risk values are provided.

This also holds for any known symmetric binary uncertainty score that is
strictly monotone in min(p(A),1-p(A)), after inverting that scalar map.
It does not hold for arbitrary unknown scales, unrelated laws across probes,
or general optimized losses without these hypotheses.

## Near-identification need not be stable

For 0<epsilon<1/10, take
p=(9/10,1/10-epsilon,epsilon) and
q=(1/10,9/10-epsilon,epsilon).
Both have three positive coordinates and are exactly identified by their
singleton risks. Their risk vectors differ in just one coordinate by
2*epsilon, but their total-variation distance is4/5. Thus no global uniform
inverse-continuity guarantee follows on this open support class as it
approaches a two-point support. A noise-aware decoder must retain the
multiple compatible branches near that boundary.

## Strong ordinary comparison

The earlier PI-7/section16 construction already shows that a known
state-dependent additive shift can make one binary proper-score optimum
strictly monotone and identify a binary law. Such shifts change the input
contract and remove the symmetric ambiguity. Therefore this note is a
classification for a natural restricted loss family, not a claim that
optimal values generally cannot identify a law or that this is the best
measurement design. Moderate novelty requires a close uncertainty-profile
or phase-retrieval comparison; no readiness forecast is assigned.

## Early literature disposition: reproduced core, park

Constantin--Doering, *A Topos Theoretic Notion of Entropy*,
[arXiv2006.03139](https://arxiv.org/pdf/2006.03139), section3.5,
PDF pages19--20, gives precisely the same normalized binary-entropy
reconstruction: choose p_i or1-p_i, sum the smaller roots, and identify
one majority coordinate unless two nonzero roots coincide. Those pages
and their argument were read. Inverting binary entropy translates its
classical step directly to the r_i used here. Their quantum reconstruction
uses additional rotated contexts, which are not permitted classical-event
queries in our contract.

**Park as a novel candidate.** The reconstruction is a reproduced existing
argument, with a useful binary-loss interpretation and a simple instability
example. No implementation or promotion forecast is warranted merely to
reconfirm it. This does not change the existing broader Q5 results.
