# Close comparison for the ordinal-feedback candidate

Codex (GPT-6), s18 DEVELOPMENT. Sources inspected October25,2026 UTC.
The late September results materially change the comparison; a claim of
the first polynomial finite-regret method would be false.

* [Oki--Sakaue, arXiv2602.01682v2](https://arxiv.org/pdf/2602.01682),
  Sections2--5 and AppendixD: the closest structural comparison. Its
  stronger rate on distinct coordinates remains the benchmark. AppendixD
  treats uncorrupted ties and identifies the difficulty with interpreting
  cycles when corruptions and ties coexist. Our matroid claim addresses
  that combination with a weaker dimension rate and a simpler path kernel.
* [Cai et al., arXiv2609.13440v1](https://arxiv.org/pdf/2609.13440),
  model, reduction and Section3.2/Theorem3.6: arbitrary compact action sets
  in the Euclidean normalization admit O(d) regret with quadratic matrix
  work plus a forward solve. The robust O(d+C) theorem needs a supplied
  corruption ceiling; the paper explicitly leaves budget-agnostic tuning
  unresolved. This is a stronger general regret baseline, not something
  our restricted result supersedes. Its proof was inspected at reduction
  and corruption-theorem scope, not independently confirmed in full.
* [Sakaue, arXiv2609.26978v1](https://arxiv.org/pdf/2609.26978), abstract
  and opening theorem scope: expected O(sqrt(d)) regret under Euclidean
  normalization, with polynomial running time left unresolved. This is
  another mandatory current comparison; no full-paper audit was performed.
* [Kitaoka, arXiv2609.09809v2](https://arxiv.org/pdf/2609.09809),
  Assumption3.1 and opening guarantees: finite mistakes under a uniform
  witness margin and unique optimum. The unknown-budget tied-feedback
  contract is not established merely by citing this assumption set.
* [Schulze2003](https://lists.gnu.org/archive/html/demexp-dev/2003-09/pdfte6xCA0eUd.pdf)
  and [Bubboloni--Gori2018](https://arxiv.org/pdf/1606.03898),
  Propositions1--2, Theorems3 and55: the ranking kernels and their strict
  transitivity are established machinery. In particular the latter already
  compares flow strength and strongest-path strength. No ranking novelty
  is claimed. [Gori2024](https://doi.org/10.1016/j.mathsocsci.2024.05.003)
  also interprets disjoint paths as robust independent arguments.
* [Shivaswamy--Joachims2015](https://www.cs.cornell.edu/~tj/publications/shivaswamy_joachims_15a.pdf),
  Sections3.1 and4 and the movie-feedback description: learning from merely
  improving ordinal feedback is established. Its general contextual regret
  guarantee and our finite named-item mistake claim have different scopes.
  Improving feedback itself is not a new interface.

## A fair stronger control obtained by rescaling ranks

For matroid bases, replacing the true component values by their integer
weak-order ranks preserves the complete set of optimal bases. This follows
from ordinary greedy optimality, including its tie groups. The rank vector
has norm at most(d-1)*sqrt(d); a basis indicator has norm at most sqrt(d).
After scaling both into unit balls, every strictly suboptimal basis has
gap at least1/[d*(d-1)] when d>1 and there is more than one utility level.

Consequently, applying the cited known-budget general regret theorem to
this observationally equivalent rank utility gives a coarse ordinary
mistake bound O(d^2*(d+C0)), plus the C0 exceptional rounds. This is our
inference from its normalized theorem, not a bound stated by those authors.
All-tied utilities have zero mistakes directly. The learner need not know
the true ranks: they are a witness in its analysis. Known C0 is still needed
for that comparator's supplied tuning. Thus even gap-independent finite
mistakes on this domain are not by themselves a sufficient novelty claim.

## Remaining plausible delta and cheapest blocker

The candidate combines arbitrary utility ties, arbitrary feasible bad
reports on an UNKNOWN finite number of rounds, changing matroids, and
the explicit binom(d,2)*(C+1)+C mistake count with a conventional cubic
path implementation. It uses no center integration, matrix precision
schedule or feedback truth test. Those are implementation facts, not a
measured performance advantage. A specialist may still view the construction
as an immediate standard corollary, or a prior robust-order result may
already supply it. That is the main remaining contribution blocker.

The next focused comparison should test that exact combination against
budget-agnostic contextual search, robust online ordering and the published
ICML version of the close structural paper. Do not spend another full
recurrence polishing optional max-flow, selective-query or M-convex
extensions before resolving this question. They are separate claims.

## Ordinary last-response caching is a strong small-context control

If at most q distinct available menus occur, store the latest reported
winner for each menu and propose it next time. There is at most one initial
mistake per menu; thereafter a mistake can occur only if that menu's previous
report was corrupted. Each bad report can cause at most one such later
mistake. Thus the simple cache makes at most q+C mistakes, without knowing
C and with arbitrary true ties. On d named alternatives there are at most
2^d-1 nonempty menus, so this already gives a finite bound with exponential
context storage and a better dependence on C. The point of pair transfer
is avoiding dependence on the number of menus, not obtaining finite mistakes
for the first time. When q is small, this cache may be preferable.

The same argument applies to compound-action contexts if stable identifiers
guarantee that the entire feasible family repeats. An arbitrary independence
oracle does not supply cheap semantic equality of contexts by itself. State
the identifier and storage contract before using this control or claiming
an advantage over it. This cache is our elementary comparator derivation,
consistent with the existing coactive literature's finite-context warning.
