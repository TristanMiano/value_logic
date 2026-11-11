# R1.3 Excellence exemplars: what diverse judges' choices of "the best" reveal

**Author:** Claude (Fable 5.2). **Date:** November 9, 2026. **Cycle:**
[P4-R1-C001](../notebook/P4-R1-C001/record.md), session 2 (cycle unfinished).
**Thesis:** C1, through the essay's tree argument (plan item W1.5).
**Status:** elementary proofs and seeded simulations by one model. Not
independently reviewed. Most ingredients are standard; see section 5.

**S6 review, Codex (GPT-6), November 10, 2026:** the invariant-exemplar
construction is retained. The low-rank interpretation, cone-count scope and
criterion-extension argument are corrected below. Original simulation records
are unchanged; see the [review](../notebook/P4-R1-C001/review_s6.md).

## What this shows

Ask many judges with different values to pick the best object.

- **The set of objects that ever get picked does not depend on who is
  judging.** Any sufficiently diverse population of judges picks from the
  same set of exemplars, which is fixed by the objects alone. The
  frequencies with which exemplars are picked do depend on the population;
  the set does not (Theorem 7(a)). This is a fact recovered from value
  judgments that is invariant to the values.
- **Shared causes reduce the dimensions through which values select
  exemplars.** If many criteria depend on a few causes, a judge's choice
  depends on a low-dimensional summary. The exemplar set is invariant when
  added criteria leave the accessible cone unchanged; a single shared
  positive ray gives one exemplar (Theorem 7(b)). A small count needs further
  geometry or distributional assumptions, as in part (c). In simulation with 5,000 objects, going
  from 2 to 16 criteria leaves 2 to 5 exemplars when two causes are shared
  and raises them from 4 to 425 when criteria are independent.
- **For Gaussian causes in the plane the count is explicit:** the expected
  number of exemplars is one plus the judges' share of directions times the
  expected number of hull vertices, for a proper sector of at most a
  half-circle. The hull count grows only like the square root of
  the logarithm of the number of objects (Theorem 7(c)).
- **Different forms of valuing reach different exemplars.** Judges who weigh
  criteria linearly never pick a balanced object that lies in a dent of the
  frontier; judges who insist on the weakest criterion pick every undominated
  object (Theorem 7(d)).

In the judgment core, objects are performers, criteria are task types, and
the map from causes to scores is the transfer kernel of R1.1. The same
kernel therefore fixes both the delineation of tasks (its twin classes) and
the kinds of excellence (the cone its rows span).

## 1. Setting

A finite set of objects $`o`$ has scores $`v_o\in\mathbb R^D`$ on $`D`$
criteria. Objects with identical scores are twins and count as one. A
**linear judge** with weights $`w\in\mathbb R^D_{>0}`$ picks a maximizer of
$`\langle w,v_o\rangle`$. A population of judges is **diverse** when its
weights have a density that is positive on the whole positive orthant.
Scores have **shared causes** when $`v_o=Bh_o`$ for causes
$`h_o\in\mathbb R^r`$ and a loading matrix $`B`$; then
$`K=\{B^{\top}w:w>0\}`$ is the cone of directions in cause space that some
value system cares about.

## 2. Results

**Theorem 7. Evidence: (a), (b), (d) proved; (c) proved given rotation
invariance, with the growth rate quoted from the literature and checked by
simulation.**

- **(a) Invariance.** Let $`E`$ be the set of objects that are the unique
  maximizer of $`\langle w,v_o\rangle`$ for some $`w>0`$. For every diverse
  population, the objects picked with positive probability are exactly those
  in $`E`$, whatever the tie-breaking rule.
- **(b) Shared causes.** If $`v_o=Bh_o`$, a judge's pick depends on $`w`$
  only through $`u=B^{\top}w`$, and $`E`$ is the set of objects that uniquely
  maximize $`\langle u,h_o\rangle`$ for some $`u\in K`$. Hence $`E`$ depends
  on the criteria only through the cone $`K`$: twin criteria and criteria
  that are positive combinations of others can be dropped without changing
  $`E`$; a new criterion can add exemplars only if its loading lies outside
  the closure of $`K`$, and it removes no strict winner when the old score
  vectors are distinct. If new criteria separate old twins, every winning
  twin class has at least one winning descendant. If $`K`$ is a single
  nonzero ray, $`E`$ has one element after quotienting score twins.
- **(c) Count.** Let the $`h_o`$ be $`N`$ independent standard Gaussian
  points in the plane, with $`N\ge3`$, and let $`K`$ be a proper sector of
  angle $`0\le\alpha\le\pi`$. Then
  $`\mathbb E|E|=1+\frac{\alpha}{2\pi}\,\mathbb E[V_N]`$, where $`V_N`$ is
  the number of vertices of the convex hull.
- **(d) Min-type judges.** Suppose no two objects share a score on any
  criterion, as holds with probability one for continuous scores, and fix a
  reference point below all scores. A judge who maximizes $`\min_d (v_{o,d}-\mathrm{ref}_d)/w_d`$ picks, as $`w`$
  ranges over a diverse population, exactly the undominated objects, each
  with positive probability. Linear judges pick only those undominated
  objects that are vertices of the convex hull of the scores.

*Proof.* (a) Uniqueness of a maximizer is a finite set of strict linear
inequalities in $`w`$, so it holds on an open set, which has positive
probability. An object outside $`E`$ is a maximizer only where it ties with
an object of different score, a subset of finitely many hyperplanes, which
has probability zero. (b) $`\langle w,Bh\rangle=\langle B^{\top}w,h\rangle`$.
The relative interior of the cone generated by the rows is unchanged by
repeating a row or adding one in its closed cone. An old strict winner
remains strict when a new criterion receives a sufficiently small positive
weight; this argument also covers an increase in the span of the cone. If
an old winning twin class splits, maximize the new criterion inside that
class, then take its weight small enough to preserve its gap over the other
classes. (c) As the direction $`u`$ sweeps
the arc, the maximizer changes exactly when $`u`$ passes the outward normal
of a hull edge, so $`|E|`$ is one plus the number of edge normals in the
arc. The law of the sample is rotation invariant, so the expected number of
edge normals in an arc is its share $`\alpha/2\pi`$ of the expected number
of edges, which equals the expected number of vertices. A sector of length
at most pi cannot revisit a vertex's normal cone. For the full plane,
instead, every hull vertex is reached and the count is $`V_N`$, without
the extra one. (d) For an
undominated $`o`$ take $`w=v_o-\mathrm{ref}`$. Then $`o`$ scores 1 and any
$`o'`$ scoring at least 1 has $`v_{o'}\ge v_o`$ in every coordinate, so
$`o'`$ is a twin of $`o`$. The inequality is strict for non-twins and
persists for nearby $`w`$. An object dominated by $`o'`$ is then
strictly below it on every criterion and scores strictly less than $`o'`$
for every $`w`$. The statement about linear
judges is (a). $`\square`$

## 3. Checks

[excellence.py](../notebook/P4-R1-C001/excellence.py), seed 20261109, output in
[excellence.json](../notebook/P4-R1-C001/excellence.json).

- **(c).** Over 300 samples each, mean exemplar counts against the formula
  with the simulated $`\mathbb E[V_N]`$: for $`N=10^3,10^4,10^5`$ and a
  90-degree cone, 3.87, 4.36, 5.02 against 3.88, 4.41, 4.89; for 10 degrees,
  1.32, 1.36, 1.39 against 1.32, 1.38, 1.43. Mean hull sizes were 11.6, 13.7
  and 15.6.
- **(a), (b).** 5,000 objects, two causes, six criteria in a 90-degree cone:
  the exact exemplar set has 4 objects. Three populations of 100,000 judges
  (evenly spread weights, concentrated weights, heavy-tailed weights) picked
  3, 4 and 4 objects, all inside that set; the population with evenly spread
  weights did not reach the fourth in its sample. Keeping only the two
  extreme criteria gave the same 4. Adding a criterion outside the cone gave
  7, including the original 4.
- **Growth with criteria** (5,000 objects, 100,000 judges; distinct objects
  picked):

  | Criteria | Two shared causes | Shared causes plus 30% idiosyncratic | Independent criteria |
  |---|---|---|---|
  | 2 | 3 | 5 | 4 |
  | 4 | 5 | 8 | 30 |
  | 8 | 4 | 7 | 120 |
  | 16 | 2 | 4 | 425 |

- **(d).** 10,000 objects with two independent criteria, 200 samples: 9.94
  undominated objects on average (the harmonic number is 9.79), of which
  linear judges can reach 4.58. In the five samples where 20,000 min-type
  judges were drawn, they picked every undominated object.

## 4. Limits

- **Low rank alone does not bound the exemplar count.** Take any N distinct
  points on the open positive quarter of the unit circle, with two criteria
  equal to their coordinates. Each point is the unique maximizer for the
  positive weight vector equal to that point: its self-inner-product is one
  and every other point has smaller inner-product. Rank two therefore
  permits all N objects to be exemplars. The Gaussian construction in (c)
  supplies a positive, distribution-dependent small-count result.
- **The frequencies are not invariant.** How often each exemplar is picked
  depends on the population of judges. Calling an exemplar a "centroid" of
  opinion is a statement about that population; membership in the exemplar
  set is the fact about the objects.
- **Exact shared causes.** With idiosyncratic components the dependence on
  $`w`$ is no longer low-dimensional, and the exemplar set grows (third
  column above). That real excellences share causes is an empirical claim
  about a domain; the growth of the picked set with the number of criteria
  is a way to test it.
- **A diverse population may not reach every exemplar in a finite sample,**
  as one population above shows.
- **Not treated:** noisy or mistaken judges; top-k lists and what a "broad"
  judge's list should cover; recovering the causes from picks alone, without
  knowing the criteria; causes that are not Gaussian or not planar, where
  the count in (c) changes.

## 5. Closest established work

Quoted from memory and not re-read in this session: the distinction between
supported and unsupported efficient points and the fact that weighted
min-type (Chebyshev) scalarizations reach all efficient points are standard
in multi-objective optimization; the expected number of hull vertices of a
planar Gaussian sample grows like $`2\sqrt{2\pi\ln N}`$ (Rényi and
Sulanke), and the expected number of undominated points among $`N`$ points
with independent coordinates in the plane is the harmonic number. The
simulated hull sizes are below the asymptotic values 13.2, 15.2 and 17.0,
consistent with slow convergence. What is added here is small: the
statement of invariance across populations of judges as the factual content
of the tree argument, the reduction to the cone of the transfer kernel, and
the link to R1.1.

The S6 review checked the fixed-dimension Gaussian facet asymptotic against
[Böröczky, Lugosi and Reitzner, *Facets of High-Dimensional Gaussian
Polytopes*, section 1](https://link.springer.com/article/10.1007/s12220-023-01440-5).
For dimension two, facets and vertices have the same count and their stated
formula gives the coefficient above. The scalarization claims were
reconstructed directly here; their full literature history has not been
reconstructed in this cycle.

## 6. Gap to the thesis

The tree argument also says that a great judge sees why the dimensions are
connected. Here that would mean recovering the loading matrix, or at least
the number of causes, from judgments. With criteria known, (b) shows picks
factor through $`B^{\top}w`$, which constrains $`B`$; an identification
statement is open. Combining this with R1.2, where judges are credited by
vindication, is also open: which exemplars does a society at a
self-confirming fixed point see?
